from sqlalchemy.orm import Mapped, mapped_column

from project.core.database import Base


class Workshop(Base):
    __tablename__ = "workshops"

    id: Mapped[int] = mapped_column(primary_key=True)

    workshop_name: Mapped[str] = mapped_column()

    workshop_type: Mapped[str] = mapped_column()

    people_count: Mapped[int] = mapped_column()
