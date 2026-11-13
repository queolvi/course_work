import pytest

from app.core.database import db
from app.repositories.batch_repo import BatchRepository


def is_db_available():
    try:
        db.connect()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not is_db_available(),
    reason="Database is not available"
)


def test_db_connection_works():
    cursor = db.get_cursor()
    cursor.execute("SELECT 1")
    result = cursor.fetchone()
    assert result[0] == 1


def test_batch_repo_returns_list():
    repo = BatchRepository()
    batches = repo.get_all()
    assert isinstance(batches, list)