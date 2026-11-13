from typing import List, Optional

from app.models.customer import Customer
from app.repositories.base_repo import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def _map_row(self, row) -> Customer:
        return Customer(
            customer_id=row.customer_id,
            name=row.name,
            contact=row.contact,
            user_id=row.user_id,
            inn=row.inn,
            city=row.city,
            street=row.street,
            building=row.building,
            apartment=row.apartment,
        )

    def get_all(self) -> List[Customer]:
        return self._fetch_all(
            "SELECT customer_id, name, contact, user_id, inn, city, street, building, apartment "
            "FROM dbo.CUSTOMERS")

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        return self._fetch_one(
            "SELECT customer_id, name, contact, user_id, inn, city, street, building, apartment "
            "FROM dbo.CUSTOMERS WHERE customer_id = ?",(customer_id,),)

    def create(
        self,
        name: str,
        contact: str,
        user_id: Optional[int] = None,
        inn: Optional[str] = None,
        city: Optional[str] = None,
        street: Optional[str] = None,
        building: Optional[str] = None,
        apartment: Optional[str] = None,) -> int:
        cursor = self._execute(
            "INSERT INTO dbo.CUSTOMERS "
            "(name, contact, user_id, inn, city, street, building, apartment) "
            "OUTPUT INSERTED.customer_id VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name, contact, user_id, inn, city, street, building, apartment),)
        self.commit()
        return cursor.fetchone().customer_id

    def update(self, customer_id: int, name: str, contact: str) -> bool:
        cursor = self._execute(
            "UPDATE dbo.CUSTOMERS SET name = ?, contact = ? WHERE customer_id = ?",
            (name, contact, customer_id),)
        self.commit()
        return cursor.rowcount > 0

    def delete(self, customer_id: int) -> bool:
        cursor = self._execute("DELETE FROM dbo.CUSTOMERS WHERE customer_id = ?", (customer_id,))
        self.commit()
        return cursor.rowcount > 0