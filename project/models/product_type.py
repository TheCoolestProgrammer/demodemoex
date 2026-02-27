from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from project.core.database import Base


class ProductType(Base):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(primary_key=True)

    product_type: Mapped[str] = mapped_column()

    product_type_coef: Mapped[Decimal] = mapped_column(DECIMAL(5, 2))
