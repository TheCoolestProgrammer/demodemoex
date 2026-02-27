from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from project.core.database import Base


class ProductWorkshop(Base):
    __tablename__ = "product_workshops"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    workshop_id: Mapped[int] = mapped_column(ForeignKey("workshops.id"))

    make_time: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
