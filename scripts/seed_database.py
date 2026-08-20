"""Load data/mock_products.json into PostgreSQL after `alembic upgrade head`."""
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from app.database import SessionLocal
from app.models.product import Product
def main():
 data=json.loads((Path(__file__).resolve().parents[1]/"data"/"mock_products.json").read_text(encoding="utf-8")); db=SessionLocal()
 try:
  if db.query(Product).count(): print("Products already exist; reset first to reseed."); return
  db.bulk_insert_mappings(Product,data); db.commit(); print(f"Seeded {len(data)} products")
 finally: db.close()
if __name__=="__main__": main()
