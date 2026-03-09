from  pydantic import BaseModel,PositiveInt
from decimal import Decimal

class AddProduct(BaseModel):
    product_type: int
    product_name: str
    articul: PositiveInt
    min_partner_cost: Decimal
    base_material: int

    # workshops: list[tuple[int, float]]

class UpdateProduct(BaseModel):
    id: int 
    product_type: int
    product_name: str
    articul: PositiveInt
    min_partner_cost: Decimal
    base_material: int