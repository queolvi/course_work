from unittest.mock import MagicMock

from app.logic.strategies.fefo_strategy import FEFOReservationStrategy
from app.logic.strategies.lifo_strategy import LIFOReservationStrategy


def test_fefo_selects_earliest_expiration_first(sample_batches):

    strategy = FEFOReservationStrategy()
    strategy.batch_repo.get_fefo_batches = MagicMock(return_value=sample_batches)
    selected = strategy.select_batches(product_id=10, quantity=80)

    assert selected[0].batch_id == 1


def test_lifo_selects_newest_manufacture_first(sample_batches):
    strategy = LIFOReservationStrategy()
    strategy.batch_repo.get_available_by_product = MagicMock(return_value=sample_batches)
    selected = strategy.select_batches(product_id=10, quantity=50)

    assert selected[0].batch_id == 3