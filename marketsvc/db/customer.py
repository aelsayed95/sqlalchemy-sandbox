from sqlalchemy.orm import Mapped, mapped_column

from marketsvc.db.base import Base, engine


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address_id: Mapped[int]

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, address_id={self.address_id!r})"
