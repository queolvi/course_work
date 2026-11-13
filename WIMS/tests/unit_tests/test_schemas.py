from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.batch_schema import BatchCreate
from app.schemas.product_schema import ProductCreate


def test_batch_create_valid_data():
    data = {
        "product_id": 1,
        "quantity": 100,
        "manufacture_date": date.today(),
        "expiration_date": date.today() + timedelta(days=30),
        "location_id": 1,
    }
    batch = BatchCreate(**data)
    assert batch.product_id == 1
    assert batch.quantity == 100


def test_batch_create_invalid_expiration():
    with pytest.raises(ValidationError):
        BatchCreate(
            product_id=1,
            quantity=100,
            manufacture_date=date.today() + timedelta(days=30),
            expiration_date=date.today(),  # раньше manufacture — ошибка
            location_id=1,
        )