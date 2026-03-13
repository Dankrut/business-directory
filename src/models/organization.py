from typing import List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.models.organization_activity import OrganizationActivityOrm

if TYPE_CHECKING:
    from .building import BuildingOrm
    from .phone import PhoneOrm
    from .activity import ActivityOrm


class OrganizationOrm(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    building: Mapped["BuildingOrm"] = relationship(
        "BuildingOrm", back_populates="organizations"
    )
    phones: Mapped[List["PhoneOrm"]] = relationship(
        "PhoneOrm", back_populates="organization", cascade="all, delete-orphan"
    )
    activities: Mapped[List["ActivityOrm"]] = relationship(
        "ActivityOrm",
        secondary=OrganizationActivityOrm.__table__,
        back_populates="organizations",
    )
