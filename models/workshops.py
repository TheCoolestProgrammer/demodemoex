from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Workshops(Base):
    __tablename__="Workshops"
    id = Column(Integer, primary_key=True)
    workshop_name = Column(String)
    workshop_type=Column(String)
    people_count = Column(Integer)

    product_workshops = relationship("ProductWorkshops", back_populates="workshops")