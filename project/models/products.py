from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from project.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)

    prouct_type_id: Mapped[int] = mapped_column(ForeignKey("product_types.id"))

    product_name: Mapped[str] = mapped_column()

    articul: Mapped[int] = mapped_column()

    min_partner_cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))

    base_material_id: Mapped[int] = mapped_column(ForeignKey("material_types.id"))
