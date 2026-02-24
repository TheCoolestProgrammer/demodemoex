from database import Base
from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

class ProductsType(Base):
    __tablename__="ProductsType"
    id = Column(Integer, primary_key=True)
    product_type=Column(String)
    product_type_coef=Column(DECIMAL)    
    products = relationship('Products', back_populates='product_types')