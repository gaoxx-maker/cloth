"""Generate deterministic, plausible mock products without third-party data."""
import json, random
from pathlib import Path
random.seed(42)
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"data"/"mock_products.json"
RULES={
 "Workwear":(["Jacket","Cargo Pants","Boots"],["Army Green","Khaki","Brown"],["Relaxed","Oversized","Wide"]),
 "Vintage":(["Jacket","Jeans","Sweater","T-Shirt"],["Blue","Brown","Burgundy","Gray"],["Regular","Relaxed","Cropped"]),
 "Streetwear":(["Hoodie","T-Shirt","Sneakers","Cargo Pants"],["Black","White","Gray","Red"],["Oversized","Relaxed","Wide"]),
 "Minimal":(["Shirt","Coat","Pants","Sneakers"],["Black","White","Gray","Beige"],["Slim","Regular","Relaxed"]),
 "Japanese":(["Shirt","Jacket","Pants","Sneakers"],["Navy","Black","Beige","Army Green"],["Relaxed","Wide","Cropped"]),
 "Korean":(["Shirt","Sweater","Coat","Pants"],["Black","White","Gray","Blue"],["Slim","Regular","Oversized"]),
 "Y2K":(["Hoodie","Jeans","Shorts","Sneakers"],["Blue","White","Red","Black"],["Wide","Cropped","Oversized"]),
 "Outdoor":(["Jacket","Pants","Boots","Shorts"],["Green","Navy","Khaki","Gray"],["Relaxed","Regular","Wide"]),
 "Techwear":(["Jacket","Cargo Pants","Boots"],["Black","Gray","Navy"],["Relaxed","Oversized","Wide"]),
 "Preppy":(["Shirt","Sweater","Coat","Pants"],["Navy","White","Beige","Burgundy"],["Slim","Regular"]),
 "Casual":(["T-Shirt","Shirt","Jeans","Sneakers"],["White","Blue","Gray","Black"],["Regular","Relaxed"]),
 "Sports":(["Hoodie","Shorts","Sneakers","T-Shirt"],["Black","White","Blue","Red"],["Regular","Relaxed","Oversized"]),
 "Formal":(["Shirt","Coat","Pants","Boots"],["Black","Navy","Gray","White"],["Slim","Regular"]),
 "Designer":(["Coat","Jacket","Boots","Sweater"],["Black","White","Burgundy","Brown"],["Cropped","Oversized","Slim"]),
 "Retro Sports":(["Jacket","T-Shirt","Sneakers","Shorts"],["Blue","Red","White","Navy"],["Regular","Relaxed"]),}
BRANDS=["Urban Archive","North Field","Morrow Studio","Canvas Club","Object 01","Sunday Standard","Nori Lab","Common Form"]
def main(count=5000):
 rows=[]
 for i in range(count):
  style,(categories,colors,fits)=random.choice(list(RULES.items())); category=random.choice(categories); color=random.choice(colors); fit=random.choice(fits); second=random.choice([s for s in RULES if s!=style])
  title=f"{style} {color} {fit} {category}"; price=random.randrange(79,899)
  rows.append({"title":title,"description":f"{color} {fit} {category}，以 {style} 为主的日常搭配单品。","brand":random.choice(BRANDS),"category":category,"subcategory":None,"price":price,"original_price":round(price*random.uniform(1.05,1.35),2),"color":color,"fit":fit,"material":random.choice(["Cotton","Denim","Wool","Nylon","Canvas"]),"season":random.choice(["Spring","Summer","Autumn","Winter","All Season"]),"gender":"Unisex","style_primary":style,"style_secondary":second,"style_tags":[style,second],"novelty_score":round(random.random(),3),"popularity_score":round(random.random(),3),"quality_score":round(random.uniform(.4,1),3),"external_product_id":f"mock-{i+1}"})
 OUT.parent.mkdir(exist_ok=True); OUT.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8"); print(f"Wrote {len(rows)} products to {OUT}")
if __name__=="__main__": main()
