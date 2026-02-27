from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from project.core.database import Base


class MaterialType(Base):
    __tablename__ = "material_types"

    id: Mapped[int] = mapped_column(primary_key=True)

    material_type: Mapped[str] = mapped_column()

    raw_materials_loss_persentage: Mapped[Decimal] = mapped_column(DECIMAL(5, 2))
