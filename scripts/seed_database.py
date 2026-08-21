"""Load generated catalog products and their simulated merchant offers into PostgreSQL."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.database import SessionLocal
from app.models.platform import Platform
from app.models.product import Product


def main() -> None:
    data = json.loads((Path(__file__).resolve().parents[1] / "data" / "mock_products.json").read_text(encoding="utf-8"))
    db = SessionLocal()
    try:
        if db.query(Product).count():
            print("Products already exist; reset first to reseed.")
            return
        platforms = {"jd": "京东模拟店", "taobao": "淘宝模拟店", "pdd": "拼多多模拟店"}
        db.add_all([Platform(code=code, name=name) for code, name in platforms.items()])
        db.flush()
        ids = {platform.code: platform.id for platform in db.query(Platform).all()}
        for row in data:
            row["platform_id"] = ids[row.pop("platform_code")]
        db.bulk_insert_mappings(Product, data)
        db.commit()
        print(f"Seeded {len(data)} products from {len(platforms)} simulated merchants")
    finally:
        db.close()


if __name__ == "__main__":
    main()
