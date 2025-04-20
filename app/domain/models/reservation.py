from sqlalchemy import Column, Integer, ForeignKey, DateTime, func,String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="pending")
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    product = relationship("Product", back_populates="reservations")
    order = relationship("Order", back_populates="reservation", uselist=False)