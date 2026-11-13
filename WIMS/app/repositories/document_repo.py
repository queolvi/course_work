from datetime import date
from typing import List, Optional

from app.models.document import document_type
from app.models.document import document_status
from app.models.document import Document

from app.repositories.base_repo import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    def _map_row(self, row) -> Document:
        return Document(
            document_id=row.document_id,
            type=row.type,
            number=row.number,
            doc_date=row.doc_date,
            user_id=row.user_id,
            status=row.status,
            created_at=row.created_at,)

    def get_all(self) -> List[Document]:
        return self._fetch_all(
            "SELECT document_id, type, number, doc_date, user_id, status, created_at "
            "FROM dbo.DOCUMENTS")

    def get_by_id(self, document_id: int) -> Optional[Document]:
        return self._fetch_one(
            "SELECT document_id, type, number, doc_date, user_id, status, created_at "
            "FROM dbo.DOCUMENTS WHERE document_id = ?",(document_id,),
        )

    def create(
        self, type: document_type, number: str, doc_date: date, user_id: int, status: document_status = "draft"
    ) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.DOCUMENTS (type, number, doc_date, user_id, status) "
            "OUTPUT INSERTED.document_id VALUES (?, ?, ?, ?, ?)",
            (type, number, doc_date, user_id, status),)
        self.commit()
        return cursor.fetchone().document_id

    def update_status(self, document_id: int, status: document_status) -> bool:
        cursor = self._execute(
            "UPDATE dbo.DOCUMENTS SET status = ? WHERE document_id = ?",
            (status, document_id),)
        self.commit()
        return cursor.rowcount > 0

    def delete(self, document_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.DOCUMENTS WHERE document_id = ?", (document_id,))
        self.commit()
        return cursor.rowcount > 0