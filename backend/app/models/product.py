from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, ForeignKey, JSON, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    brand: Mapped[str] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    subcategory: Mapped[str | None] = mapped_column(String(80), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    original_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    color: Mapped[str] = mapped_column(String(50), index=True)
    fit: Mapped[str] = mapped_column(String(50))
    material: Mapped[str] = mapped_column(String(80))
    season: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(30), default="Unisex")
    style_primary: Mapped[str] = mapped_column(String(80), index=True)
    style_secondary: Mapped[str | None] = mapped_column(String(80), nullable=True)
    style_tags: Mapped[list[str]] = mapped_column(JSON, default=list)
    novelty_score: Mapped[float] = mapped_column(default=0.5)
    popularity_score: Mapped[float] = mapped_column(default=0.5)
    quality_score: Mapped[float] = mapped_column(default=0.5)
    platform_id: Mapped[int | None] = mapped_column(ForeignKey("platforms.id"), nullable=True)
    external_product_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    product_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
