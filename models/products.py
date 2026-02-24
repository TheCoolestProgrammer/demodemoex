from database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,DECIMAL
from sqlalchemy.orm import relationship

class Products(Base):
    __tablename__="Products"
    id = Column(Integer, primary_key=True)
    prouct_type =Column(Integer, ForeignKey("ProductsType.id"))
    product_name= Column(String)
    articul=Column(Integer)
    min_partner_cost=Column(DECIMAL)
    base_material = Column(Integer,ForeignKey("MaterialType.id"))
   
    product_types = relationship('ProductsType', back_populates='products')
    materials = relationship('MaterialType', back_populates='base_materials')
    
    product_workshops = relationship("ProductWorkshops", back_populates="products")
