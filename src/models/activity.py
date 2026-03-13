from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base

if TYPE_CHECKING:
    from .organization import OrganizationOrm


class ActivityOrm(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )
    level: Mapped[int] = mapped_column(nullable=False)
    parent: Mapped[Optional["ActivityOrm"]] = relationship(
        "ActivityOrm", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["ActivityOrm"]] = relationship(
        "ActivityOrm", back_populates="parent"
    )
    organizations: Mapped[List["OrganizationOrm"]] = relationship(
        "OrganizationOrm",
        secondary="organization_activities",
        back_populates="activities",
    )
