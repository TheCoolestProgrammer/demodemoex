from fastapi import Depends, FastAPI, Request, Form, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text, Select
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse

from models import ProductWorkshops, Products, ProductsType, MaterialType
from schemas.products import AddProduct, UpdateProduct

templates = Jinja2Templates(directory='templates')

app = FastAPI(title="main")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def main(request: Request, db:Session=Depends(get_db)):
    data={"products":[]}
    # products = db.query(ProductWorkshops).distinct(ProductWorkshops.product).all()
    # for product in products:
    #     print(product.product)
    #     data['products'].append({
    #         "product_type":product.products.product_types.product_type,
    #         "product_name":product.products.product_name,
    #         "articul":product.products.articul,
    #         "min_partner_cost":product.products.min_partner_cost,
    #         "hours":get_hours_by_id(product.product, db),
    #         "base_material":product.products.materials.material_type,
    #         "product_id":product.product
    #     })
    products = db.query(Products).all()
    for product in products:
        data['products'].append({
            "product_type":product.product_types.product_type,
            "product_name":product.product_name,
            "articul":product.articul,
            "min_partner_cost":product.min_partner_cost,
            "hours":get_hours_by_id(product.id, db),
            "base_material":product.materials.material_type,
            "product_id":product.id
        })
    
    return templates.TemplateResponse(
        request=request,
        name='main.html',
        context={"data":data}
    )

def get_hours_by_id(product_id:int, db):
    stmt = text('select sum(make_time) from "ProductWorkshops" where product=:product_id;')
    result = db.execute(stmt, {"product_id":product_id})
    return result.scalar()

@app.get('/add_product')
def add_product_get(request:Request, db:Session=Depends(get_db)):
    product_types=[]
    material_types=[]
    pt = db.query(ProductsType).all()
    for i in pt:
        product_types.append((i.id, i.product_type))
    mt = db.query(MaterialType).all()
    for i in mt:
        material_types.append((i.id, i.material_type))
    return templates.TemplateResponse(
        request=request,
        name='add_product.html',
        context={"product_types":product_types, "material_types":material_types}
    )

@app.post('/add_product')
def add_product_post(product_request:AddProduct = Form(), db:Session=Depends(get_db)):
    try:
        product_new = Products(
            prouct_type=product_request.product_type,
            product_name=product_request.product_name,
            articul=product_request.articul,
            min_partner_cost= product_request.min_partner_cost,
            base_material = product_request.base_material
        )
        db.add(product_new)
        db.commit()
        return JSONResponse(status_code=status.HTTP_201_CREATED,content=[])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,content=[])
    
@app.get('/update_product/{product_id}')
def update_product_get(product_id:int, request:Request, db:Session=Depends(get_db)):
    product_types=[]
    material_types=[]
    product = db.query(Products).where(Products.id==product_id).first()
    if not product:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={'message':'пользователь с данным id не найден'})
    pt = db.query(ProductsType).all()
    for i in pt:
        product_types.append((i.id, i.product_type))
    mt = db.query(MaterialType).all()
    for i in mt:
        material_types.append((i.id, i.material_type))
    
    return templates.TemplateResponse(
        request=request,
        name='update_product.html',
        context={
            "product_types":product_types, 
            "material_types":material_types,
            "product_id":product_id,
            "product_type_id":product.prouct_type,
            "base_material_id":product.base_material,
            "product_name":product.product_name,
            "articul":product.articul,
            "min_partner_cost":product.min_partner_cost
            }
    )

@app.post('/update_product/{product_id}', status_code=201)
def update_product_post(product_id:int, product_request:UpdateProduct=Form(), db:Session=Depends(get_db)):
    product = db.query(Products).where(Products.id == product_request.id).first()
    if not product:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content=[])
    try:
        product.prouct_type = product_request.product_type
        product.product_name = product_request.product_name,
        product.articul = product_request.articul
        product.base_material = product_request.base_material
        product.min_partner_cost = product_request.min_partner_cost
        db.commit()
        db.refresh(product)
        return JSONResponse(status_code=status.HTTP_201_CREATED,content=[])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=[])
    
@app.get('/workshops/{product_id}')
def get_workshops(product_id:int,request:Request, db:Session=Depends(get_db)):
    workshops = db.query(ProductWorkshops).where(ProductWorkshops.product == product_id).all()
    data = []
    for workshop in workshops:
        data.append({
            "make_time":workshop.make_time,
            "workshop_name":workshop.workshops.workshop_name,
            "people_count": workshop.workshops.people_count
        })   
    return templates.TemplateResponse(
        request=request,
        name='workshops.html',
        context={"data":data}
    )

@app.get('raw_materails_counter')
def get_raw_materials_count(product_type_id:int, material_type_id:int, amount:int, param1:float, param2:float ,db:Session=Depends(get_db)):
    if type(amount) is not int or amount <0:
        return -1
    if type(param1) is not float or param1<0:
        return -1
    if type(param2) is not float or param2<0:
        return -1
    pt = db.query(ProductsType).where(ProductsType.id==product_type_id).first()
    if not pt:
        return -1
    mt = db.query(MaterialType).where(MaterialType.material_type==material_type_id).first()
    if not mt:
        return -1
    c = param1*param2*pt.product_type_coef*amount
    res = c*mt.raw_materials_loss_persentage+c
    return res