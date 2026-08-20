from pydantic import BaseModel, ConfigDict, Field


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    brand: str
    category: str
    price: float
    color: str
    fit: str
    style_primary: str
    style_secondary: str | None = None
    style_tags: list[str] = Field(default_factory=list)
    novelty_score: float
    quality_score: float
    image_url: str | None = None
