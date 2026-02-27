import pandas
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from project import models
from project.core.database import AsyncSessionLocal


async def _fill_material_types(session: AsyncSession):
    df = pandas.read_excel("./etc/Material_type_import.xlsx")
    values = []
    existing_types = {
        mt.material_type: mt
        for mt in (await session.execute(select(models.MaterialType))).scalars().all()
    }
    for row in df.values.tolist():
        if row[0] in existing_types:
            continue

        values.append(
            {
                models.MaterialType.material_type: row[0],
                models.MaterialType.raw_materials_loss_persentage: row[1],
            }
        )
    if len(values) > 0:
        stmt = insert(models.MaterialType).values(values)
        await session.execute(stmt)


async def _fill_product_types(session: AsyncSession):
    df = pandas.read_excel("./etc/Product_type_import.xlsx")
    values = []
    existing_types = {
        pt.product_type: pt
        for pt in (await session.execute(select(models.ProductType))).scalars().all()
    }
    for row in df.values.tolist():
        if row[0] in existing_types:
            continue

        values.append(
            {
                models.ProductType.product_type: row[0],
                models.ProductType.product_type_coef: row[1],
            }
        )
    if len(values) > 0:
        stmt = insert(models.ProductType).values(values)
        await session.execute(stmt)


async def _fill_workshops(session: AsyncSession):
    df = pandas.read_excel("./etc/Workshops_import.xlsx")
    existing_shops = {
        w.workshop_name: w for w in (await session.execute(select(models.Workshop))).scalars().all()
    }
    values = []

    for row in df.values.tolist():
        if row[0] in existing_shops:
            continue

        values.append(
            {
                models.Workshop.workshop_name: row[0],
                models.Workshop.workshop_type: row[1],
                models.Workshop.people_count: row[2],
            }
        )
    if len(values) > 0:
        stmt = insert(models.Workshop).values(values)
        await session.execute(stmt)


async def _fill_products(session: AsyncSession):
    df = pandas.read_excel("./etc/Products_import.xlsx")

    product_types = {
        pt.product_type: pt
        for pt in (await session.execute(select(models.ProductType))).scalars().all()
    }

    material_types = {
        mt.material_type: mt
        for mt in (await session.execute(select(models.MaterialType))).scalars().all()
    }
    existing_products = {
        p.product_name: p for p in (await session.execute(select(models.Product))).scalars().all()
    }
    values = []
    for row in df.values.tolist():
        if row[1] in existing_products:
            continue

        product_type = product_types.get(row[0])
        if not product_type:
            print(f"product type: {row[0]} not found")
            continue

        material_type = material_types.get(row[4])
        if not material_type:
            print(f"material type: {row[4]} not found")
            continue

        values.append(
            {
                models.Product.prouct_type_id: product_type.id,
                models.Product.product_name: row[1],
                models.Product.articul: row[2],
                models.Product.min_partner_cost: row[3],
                models.Product.base_material_id: material_type.id,
            }
        )
    if len(values) > 0:
        stmt = insert(models.Product).values(values)
        await session.execute(stmt)


async def _fill_product_workshops(session: AsyncSession):
    df = pandas.read_excel("./etc/Product_workshops_import.xlsx")

    products = {
        p.product_name: p for p in (await session.execute(select(models.Product))).scalars().all()
    }

    workshops = {
        w.workshop_name: w for w in (await session.execute(select(models.Workshop))).scalars().all()
    }

    existing_relations: dict[tuple[int, int], models.ProductWorkshop] = {
        (pw.product_id, pw.workshop_id): pw
        for pw in (await session.execute(select(models.ProductWorkshop))).scalars().all()
    }

    values = []
    for row in df.values.tolist():
        product = products.get(row[0])
        if not product:
            print(f"product: {row[0]} not found")
            continue

        workshop = workshops.get(row[1])
        if not workshop:
            print(f"workshop: {row[1]} not found")
            continue

        if (product.id, workshop.id) in existing_relations:
            continue

        values.append(
            {
                models.ProductWorkshop.product_id: product.id,
                models.ProductWorkshop.workshop_id: workshop.id,
                models.ProductWorkshop.make_time: row[2],
            }
        )
    if len(values) > 0:
        stmt = insert(models.ProductWorkshop).values(values)
        await session.execute(stmt)


async def fill_data():
    async with AsyncSessionLocal() as session:
        await _fill_product_types(session)
        await _fill_material_types(session)
        await _fill_products(session)
        await _fill_workshops(session)
        await _fill_product_workshops(session)

        await session.commit()
