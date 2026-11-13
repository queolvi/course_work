from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    
    name: str = Field(..., min_length=1, max_length=255, description="name description")
    stock_keeping_unit: str = Field(
        ..., 
        min_length=1, 
        max_length=50, 
        description="SKU"
    )
    category_id: int = Field(..., gt=0, description="category id")
    unit: str = Field(..., max_length=20, description="unit of measurements")
    description: str | None = Field(None, max_length=500)
    min_stock: int = Field(0, ge=0, le=100_000, description="minimum stock")