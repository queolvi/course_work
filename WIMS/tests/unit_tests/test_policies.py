"""Тесты паттерна Policy (Default, VIP, AutoWriteOff)."""
from datetime import date, timedelta

from app.logic.policies.default_reservation_policy import DefaultReservationPolicy
from app.logic.policies.auto_write_off_policy import AutoWriteOffPolicy
from app.models.batch import Batch


def test_default_policy_validates_quantity(sample_user):
    policy = DefaultReservationPolicy()
    assert policy.validate(50, sample_user) is True
    assert policy.validate(101, sample_user) is False


def test_auto_write_off_allows_expired_batch_without_reservations():
    policy = AutoWriteOffPolicy()
    batch = Batch(
        batch_id=1, product_id=1, quantity=100, reserved_quantity=0,
        manufacture_date=date.today() - timedelta(days=60),
        expiration_date=date.today() - timedelta(days=1),  # просрочена
        location_id=1,
    )
    assert policy.can_write_off(batch) is True