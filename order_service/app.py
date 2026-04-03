from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Order
from producer import publish_order
from grpc_client import get_product_via_grpc
import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/order/{product_id}")
def create_order(product_id: int, db: Session = Depends(get_db)):
    product = get_product_via_grpc(product_id)

    if not product:
        return {"error": "Product not found"}
    order = Order(
        product_id=product_id,
        product_name=product["name"],
        price=product["price"],
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    publish_order(product_id)

    return {
        "message": "Order created and saved to database!",
        "order_id": order.id,
        "product": product["name"],
        "price": product["price"],
        "status": order.status
    }

@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return {"orders": orders}