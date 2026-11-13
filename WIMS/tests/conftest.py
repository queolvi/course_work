import sys
from pathlib import Path
from datetime import date, timedelta

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.batch import Batch
from app.models.user import User


@pytest.fixture
def sample_user():
    return User(
        user_id=1,
        username="test_user",
        password_hash="hash123",
        full_name="Test User",
        role_id=1,
        is_active=True,
    )


@pytest.fixture
def sample_batches():
    today = date.today()
    return [
        Batch(
            batch_id=1, product_id=10, quantity=100, reserved_quantity=0,
            manufacture_date=today - timedelta(days=30),
            expiration_date=today + timedelta(days=30),
            location_id=1,
        ),
        Batch(
            batch_id=2, product_id=10, quantity=50, reserved_quantity=0,
            manufacture_date=today - timedelta(days=10),
            expiration_date=today + timedelta(days=10),  # самая ранняя просрочка
            location_id=1,
        ),
        Batch(
            batch_id=3, product_id=10, quantity=200, reserved_quantity=0,
            manufacture_date=today - timedelta(days=5),
            expiration_date=today + timedelta(days=60),
            location_id=1,
        ),
    ]