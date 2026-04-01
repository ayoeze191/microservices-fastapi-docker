from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Order(Base):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True, index=True)
    product_id   = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    price        = Column(Float, nullable=False)
    status       = Column(String, default="pending")
    created_at   = Column(DateTime, server_default=func.now())