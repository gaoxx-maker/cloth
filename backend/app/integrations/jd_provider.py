"""Low-volume adapter for a JD product-search endpoint.

The endpoint differs by JD API product, so its URL and request parameter names are
environment settings.  This module deliberately keeps supplier fields out of the
application contract and never lets a supplier outage affect virtual products.
"""

from __future__ import annotations

import hashlib
import json
import time
from functools import lru_cache
from threading import Lock
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.config import Settings
from app.integrations.base import ProductProvider
from app.schemas.product import ProductRead


class JDProvider(ProductProvider):
    """Search JD sparingly, with a process-local cache and request throttle."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self._cache: dict[str, tuple[float, list[ProductRead]]] = {}
        self._last_request_at = 0.0
        self._lock = Lock()

    def should_enrich(self, query: str) -> bool:
        """Use a stable query hash so only roughly the configured percentage calls JD."""
        if not (self.settings.jd_enabled and self.settings.jd_api_key and self.settings.jd_api_url):
            return False
        ratio = max(0, min(100, self.settings.jd_search_ratio_percent))
        if ratio == 0:
            return False
        bucket = int(hashlib.sha256(query.casefold().encode()).hexdigest()[:8], 16) % 100
        return bucket < ratio

    def search_products(self, query: str) -> list[ProductRead]:
        if not self.should_enrich(query):
            return []
        normalized_query = query.strip()
        now = time.monotonic()
        with self._lock:
            cached = self._cache.get(normalized_query)
            if cached and now - cached[0] < self.settings.jd_min_request_interval_seconds:
                return cached[1]
            if now - self._last_request_at < self.settings.jd_min_request_interval_seconds:
                return []
            self._last_request_at = now
        try:
            products = self._request_search(normalized_query)
        except Exception:
            # A limited or unavailable third-party API must never break local search.
            return []
        with self._lock:
            self._cache[normalized_query] = (now, products)
        return products

    def get_product(self, external_id: str) -> ProductRead | None:
        # Product detail is intentionally kept in the virtual library.  Remote
        # search items link to JD via their own URL when that API provides one.
        return None

    def _request_search(self, query: str) -> list[ProductRead]:
        params = {
            self.settings.jd_query_param: query,
            self.settings.jd_api_key_param: self.settings.jd_api_key,
            "limit": self.settings.jd_max_products_per_search,
        }
        separator = "&" if "?" in self.settings.jd_api_url else "?"
        url = f"{self.settings.jd_api_url}{separator}{urlencode(params)}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "FashionExplorer/0.2"})
        with urlopen(request, timeout=4) as response:  # nosec B310: URL is an operator-supplied setting
            payload = json.loads(response.read().decode("utf-8"))
        return self._normalize_results(payload, query)[: self.settings.jd_max_products_per_search]

    def _normalize_results(self, payload: Any, query: str) -> list[ProductRead]:
        items = self._extract_items(payload)
        return [self._normalize_item(item, query) for item in items if isinstance(item, dict)]

    @staticmethod
    def _extract_items(payload: Any) -> list[Any]:
        if isinstance(payload, list):
            return payload
        if not isinstance(payload, dict):
            return []
        for container in (payload, payload.get("data", {}), payload.get("result", {})):
            if isinstance(container, list):
                return container
            if isinstance(container, dict):
                for key in ("items", "list", "products", "goods", "data"):
                    value = container.get(key)
                    if isinstance(value, list):
                        return value
        return []

    @staticmethod
    def _value(item: dict[str, Any], *names: str, default: Any = "") -> Any:
        return next((item[name] for name in names if item.get(name) not in (None, "")), default)

    def _normalize_item(self, item: dict[str, Any], query: str) -> ProductRead:
        external_id = str(self._value(item, "skuId", "sku_id", "id", "goodsId", "goods_id", default=query))
        product_id = -(int(hashlib.sha256(f"jd:{external_id}".encode()).hexdigest()[:12], 16) % 2_000_000_000 + 1)
        price = self._value(item, "price", "salePrice", "sale_price", "jdPrice", "jd_price", default=0)
        try:
            price = float(str(price).replace("¥", "").replace(",", ""))
        except (TypeError, ValueError):
            price = 0.0
        title = str(self._value(item, "name", "title", "goodsName", "skuName", default="京东商品"))
        image_url = self._value(item, "imageUrl", "image_url", "image", "picUrl", "imagePath", default=None)
        return ProductRead(
            id=product_id, title=title, description=str(self._value(item, "description", "desc", default=title)),
            brand=str(self._value(item, "brandName", "brand", default="京东")),
            category=str(self._value(item, "categoryName", "category", default="服饰")), price=price,
            color=str(self._value(item, "color", default="未知")), fit="常规", style_primary="Casual",
            style_tags=["京东", "实时补充"], novelty_score=0.5, quality_score=0.5, image_url=str(image_url) if image_url else None,
        )


@lru_cache
def get_jd_provider() -> JDProvider:
    """Keep the cache and global request cooldown across HTTP requests."""
    from app.config import get_settings

    return JDProvider(get_settings())
