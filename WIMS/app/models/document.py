from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from enum import Enum

class document_type(Enum):
    invoice
    waybill
    write_off_act

class document_status(Enum):
    draft
    approved
    cancelled

@dataclass
class Document:
    document_id: int
    type: Optional[document_type] = None
    number: str
    doc_date: date
    user_id: int
    status: Optional[document_status] = "draft"  
    created_at: Optional[datetime] = None

    def __str__(self) -> str:
        return f"Document(id={self.document_id}, type={self.type}, number={self.number})"