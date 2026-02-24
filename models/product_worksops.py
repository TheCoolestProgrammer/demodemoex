from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

class ProductWorkshops(Base):
    __tablename__="ProductWorkshops"
    id = Column(Integer, primary_key=True)
    product = Column(Integer,ForeignKey("Products.id"))
    workshop = Column(Integer, ForeignKey("Workshops.id"))
    make_time = Column(DECIMAL)

    products = relationship("Products", back_populates="product_workshops")
    workshops = relationship("Workshops",back_populates="product_workshops")