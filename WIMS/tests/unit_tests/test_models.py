from datetime import date, timedelta
from app.models.batch import Batch


def test_batch_available_quantity():
    batch = Batch(
        batch_id=1, product_id=1, quantity=100, reserved_quantity=30,
        manufacture_date=date.today(),
        expiration_date=date.today() + timedelta(days=30),
        location_id=1,
    )
    assert batch.available_quantity == 70


def test_batch_is_expired():
    batch = Batch(
        batch_id=1, product_id=1, quantity=100, reserved_quantity=0,
        manufacture_date=date.today() - timedelta(days=60),
        expiration_date=date.today() - timedelta(days=1),
        location_id=1,
    )
    assert batch.is_expired is True
    assert batch.days_until_expiration < 0