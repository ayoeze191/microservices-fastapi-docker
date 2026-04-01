from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Product
import models

# Create tables automatically on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Seed some products on startup
@app.on_event("startup")
def seed_products():
    db = next(get_db())
    if db.query(Product).count() == 0:
        db.add_all([
            Product(name="Laptop", price=999, stock=10),
            Product(name="Smartphone", price=499, stock=20)
        ])
        db.commit()
        print("Products seeded! ✅", flush=True)

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return {"products": db.query(Product).all()}

@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product}

@app.post("/products")
def create_product(name: str, price: float, stock: int, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, stock=stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"product": product}