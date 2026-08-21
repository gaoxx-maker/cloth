"""Generate deterministic catalog products with three simulated merchant offers."""
import json
import random
from pathlib import Path

random.seed(42)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "mock_products.json"
RULES = {
    "Workwear": (["Jacket", "Cargo Pants", "Boots"], ["Army Green", "Khaki", "Brown"], ["Relaxed", "Oversized", "Wide"]),
    "Vintage": (["Jacket", "Jeans", "Sweater", "T-Shirt"], ["Blue", "Brown", "Burgundy", "Gray"], ["Regular", "Relaxed", "Cropped"]),
    "Streetwear": (["Hoodie", "T-Shirt", "Sneakers", "Cargo Pants"], ["Black", "White", "Gray", "Red"], ["Oversized", "Relaxed", "Wide"]),
    "Minimal": (["Shirt", "Coat", "Pants", "Sneakers"], ["Black", "White", "Gray", "Beige"], ["Slim", "Regular", "Relaxed"]),
    "Japanese": (["Shirt", "Jacket", "Pants", "Sneakers"], ["Navy", "Black", "Beige", "Army Green"], ["Relaxed", "Wide", "Cropped"]),
    "Korean": (["Shirt", "Sweater", "Coat", "Pants"], ["Black", "White", "Gray", "Blue"], ["Slim", "Regular", "Oversized"]),
    "Y2K": (["Hoodie", "Jeans", "Shorts", "Sneakers"], ["Blue", "White", "Red", "Black"], ["Wide", "Cropped", "Oversized"]),
    "Outdoor": (["Jacket", "Pants", "Boots", "Shorts"], ["Green", "Navy", "Khaki", "Gray"], ["Relaxed", "Regular", "Wide"]),
    "Techwear": (["Jacket", "Cargo Pants", "Boots"], ["Black", "Gray", "Navy"], ["Relaxed", "Oversized", "Wide"]),
    "Preppy": (["Shirt", "Sweater", "Coat", "Pants"], ["Navy", "White", "Beige", "Burgundy"], ["Slim", "Regular"]),
    "Casual": (["T-Shirt", "Shirt", "Jeans", "Sneakers"], ["White", "Blue", "Gray", "Black"], ["Regular", "Relaxed"]),
    "Sports": (["Hoodie", "Shorts", "Sneakers", "T-Shirt"], ["Black", "White", "Blue", "Red"], ["Regular", "Relaxed", "Oversized"]),
    "Formal": (["Shirt", "Coat", "Pants", "Boots"], ["Black", "Navy", "Gray", "White"], ["Slim", "Regular"]),
    "Designer": (["Coat", "Jacket", "Boots", "Sweater"], ["Black", "White", "Burgundy", "Brown"], ["Cropped", "Oversized", "Slim"]),
    "Retro Sports": (["Jacket", "T-Shirt", "Sneakers", "Shorts"], ["Blue", "Red", "White", "Navy"], ["Regular", "Relaxed"]),
}
BRANDS = ["Urban Archive", "North Field", "Morrow Studio", "Canvas Club", "Object 01", "Sunday Standard", "Nori Lab", "Common Form"]
MERCHANTS = [("jd", "京东模拟店", 1.00), ("taobao", "淘宝模拟店", 0.96), ("pdd", "拼多多模拟店", 0.91)]


def main(count: int = 1800) -> None:
    rows = []
    for i in range(count):
        style, (categories, colors, fits) = random.choice(list(RULES.items()))
        category, color, fit = random.choice(categories), random.choice(colors), random.choice(fits)
        second = random.choice([candidate for candidate in RULES if candidate != style])
        price, catalog_id = random.randrange(79, 899), f"mock-{i + 1:05d}"
        base = {
            "title": f"{style} {color} {fit} {category}",
            "description": f"{color} {fit} {category}，以 {style} 为主的日常搭配单品。",
            "brand": random.choice(BRANDS), "category": category, "subcategory": None,
            "color": color, "fit": fit, "material": random.choice(["Cotton", "Denim", "Wool", "Nylon", "Canvas"]),
            "season": random.choice(["Spring", "Summer", "Autumn", "Winter", "All Season"]), "gender": "Unisex",
            "style_primary": style, "style_secondary": second, "style_tags": [style, second],
            "novelty_score": round(random.random(), 3), "popularity_score": round(random.random(), 3), "quality_score": round(random.uniform(.4, 1), 3),
        }
        for code, _, factor in MERCHANTS:
            merchant_price = round(price * factor, 2)
            rows.append({**base, "price": merchant_price, "original_price": round(merchant_price * random.uniform(1.05, 1.25), 2), "platform_code": code, "external_product_id": f"{catalog_id}:{code}", "product_url": f"/merchant/{code}/{catalog_id}"})
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} mock merchant offers for {count} catalog products to {OUT}")


if __name__ == "__main__":
    main()
