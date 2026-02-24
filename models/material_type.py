from database import Base
from sqlalchemy import Column, Integer, String,DECIMAL
from sqlalchemy.orm import relationship

class MaterialType(Base):
    __tablename__="MaterialType"
    id = Column(Integer, primary_key=True)
    material_type = Column(String)
    raw_materials_loss_persentage = Column(DECIMAL)
    base_materials = relationship('Products', back_populates='materials')