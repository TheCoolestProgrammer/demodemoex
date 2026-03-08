from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import text, Select
from fastapi.templating import Jinja2Templates

from models import ProductWorkshops

templates = Jinja2Templates(directory='templates')

app = FastAPI(title="main")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
def main(request: Request, db:Session=Depends(get_db)):
    data={"products":[]}
    products = db.query(ProductWorkshops).distinct(ProductWorkshops.product).all()
    for product in products:
        data['products'].append({
            "product_type":product.products.product_types.product_type,
            "product_name":product.products.product_name,
            "articul":product.products.articul,
            "min_partner_cost":product.products.min_partner_cost,
            "hours":get_hours_by_id(product.product, db),
            "base_material":product.products.materials.material_type
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