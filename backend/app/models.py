from sqlalchemy import Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class University(Base):
    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    official_name: Mapped[str] = mapped_column(String(512), nullable=False)
    english_name: Mapped[str | None] = mapped_column(String(512), nullable=True)
    region: Mapped[str] = mapped_column(String(64), nullable=False)
    country: Mapped[str] = mapped_column(String(128), nullable=False)
    website: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)

    __table_args__ = (
        Index("ix_universities_region_country", "region", "country"),
        Index("ix_universities_official_name", "official_name"),
        Index("ix_universities_english_name", "english_name"),
    )
