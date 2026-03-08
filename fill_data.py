from database import *
import pandas
from models import *
from sqlalchemy import insert, select
from database import Base, engine

Base.metadata.create_all(bind=engine)
db = SessionLocal()

df = pandas.read_excel('./etc/Material_type_import.xlsx')
for row in df.values.tolist():
    # print(row[0],row[1])
    stmt = insert(MaterialType).values(material_type=row[0], raw_materials_loss_persentage=row[1])
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

df = pandas.read_excel('./etc/Product_type_import.xlsx')
for row in df.values.tolist():
    # print(row[0],row[1])
    stmt = insert(ProductsType).values(product_type=row[0],  product_type_coef=row[1])
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

df = pandas.read_excel('./etc/Workshops_import.xlsx')
for row in df.values.tolist():
    # print(row[0],row[1])
    stmt = insert(Workshops).values(workshop_name=row[0],  workshop_type=row[1], people_count=row[2])
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()

df = pandas.read_excel('./etc/Products_import.xlsx')
for row in df.values.tolist():
    # print(row[0],row[1])
    product_type=db.query(ProductsType).filter(ProductsType.product_type==row[0]).first()
    base_material=db.query(MaterialType).filter(MaterialType.material_type==row[4]).first()
    stmt = insert(Products).values(prouct_type=product_type.id,  product_name=row[1], articul=row[2], min_partner_cost=row[3], base_material=base_material.id)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()     
    # print(product_type.product_type)
    
df = pandas.read_excel('./etc/Product_workshops_import.xlsx')
for row in df.values.tolist():
    # print(row[0],row[1])
    product = db.query(Products).filter(Products.product_name==row[0]).first()
    workshop = db.query(Workshops).filter(Workshops.workshop_name==row[1]).first()
    # print(product)
    stmt = insert(ProductWorkshops).values(product=product.id,  workshop=workshop.id, make_time=row[2])
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()



