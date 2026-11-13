from unittest.mock import MagicMock

import pytest

from app.logic.strategies.fefo_strategy import FEFOReservationStrategy
from app.logic.policies.default_reservation_policy import DefaultReservationPolicy
from app.logic.reservation_service import ReservationService


def test_reservation_service_creates_reservation(sample_user, sample_batches):
    strategy = FEFOReservationStrategy()
    strategy.select_batches = MagicMock(return_value=sample_batches)

    policy = DefaultReservationPolicy()

    service = ReservationService(strategy, policy)
    service.reservation_repo = MagicMock()
    service.reservation_repo.create = MagicMock(return_value=100)
    service.reservation_repo.get_by_id = MagicMock(return_value=MagicMock(
        reservation_id=100, batch_id=1, quantity=50
    ))
    service.batch_repo = MagicMock()
    service.batch_repo.increase_reserved = MagicMock(return_value=True)

    reservations = service.create_reservation(product_id=10, quantity=80, user=sample_user)
    assert len(reservations) > 0


def test_reservation_service_rejects_policy_violation(sample_user):
    
    strategy = FEFOReservationStrategy()
    policy = DefaultReservationPolicy()
    service = ReservationService(strategy, policy)

    with pytest.raises(ValueError, match="policy violated"):
        service.create_reservation(product_id=10, quantity=200, user=sample_user)