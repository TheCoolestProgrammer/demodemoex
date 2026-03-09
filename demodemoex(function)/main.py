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