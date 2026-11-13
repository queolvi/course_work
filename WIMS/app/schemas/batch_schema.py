from datetime import date
from pydantic import BaseModel, Field, field_validator


class BatchCreate(BaseModel):
    
    product_id: int = Field(..., gt=0, description="product identificator")
    quantity: int = Field(..., gt=0, le=1_000_000, description="quantity of products")
    reserved_quantity: int = Field(0, ge=0, description="Reserved")
    manufacture_date: date = Field(..., description="Manufacture date")
    expiration_date: date = Field(..., description="Expiration date")
    location_id: int = Field(..., gt=0, description="identificator storage locations")

    @field_validator("expiration_date")
    @classmethod
    def expiration_must_be_after_manufacture(cls, v, info):
        if "manufacture_date" in info.data and v <= info.data["manufacture_date"]:
            raise ValueError("Expiration date must be after manufacture date")
        return v

    @field_validator("expiration_date")
    @classmethod
    def expiration_must_be_in_future(cls, v):
        if v < date.today():
            raise ValueError("Expiration date must be in the future")
        return v


class BatchUpdate(BaseModel):
    batch_id: int = Field(..., gt=0)
    new_quantity: int = Field(..., gt=0, le=1_000_000)