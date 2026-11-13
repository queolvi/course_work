from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator


class ReservationCreate(BaseModel):
    
    batch_id: int = Field(..., gt=0, description="batch identification")
    user_id: int = Field(..., gt=0, description="user identification")
    quantity: int = Field(..., gt=0, le=100_000, description="quantity for reservation")
    order_id: int | None = Field(None, gt=0, description="identification order")
    duration_hours: int = Field(24, gt=0, le=168, description="duration hours")

    @field_validator("duration_hours")
    @classmethod
    def validate_duration(cls, v):
        if v < 1 or v > 168:
            raise ValueError("Duration must be between 1 and 168 hours")
        return v

    def get_expires_at(self) -> datetime:
        return datetime.now() + timedelta(hours=self.duration_hours)