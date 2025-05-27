from datetime import datetime
from sqlalchemy import MetaData, create_engine, Table, Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from dataclasses import dataclass

db_url = "sqlite:///data.db"
engine = create_engine(db_url, echo=True)
metadata = MetaData()

entries_table = Table(
    "entries",
    metadata,
    Column("id", String, primary_key=True),  # UUID stocké en string car SQLite ne gère pas UUID nativement
    Column("name", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("category", String, nullable=True),
    Column("date", DateTime, nullable=False, default=datetime.utcnow),
)

def init_db():
    metadata.create_all(engine)

@dataclass
class Entry:
    id: uuid.UUID
    name: str
    amount: float
    category: str | None
    date: datetime

    @classmethod
    def from_db(cls, id: str, name: str, amount: float, category: str | None, date: datetime):
        return cls(
            uuid.UUID(id),  # conversion string -> UUID
            name,
            amount,
            category,
            date,
        )

def create_entry(name: str, amount: float, category: str | None = None):
    with engine.begin() as conn:
        conn.execute(
            entries_table.insert().values(
                id=str(uuid.uuid4()),  # conversion UUID -> string
                name=name,
                amount=amount,
                category=category,
                date=datetime.utcnow()
            )
        )

def get_entry(id: uuid.UUID):
    with engine.begin() as conn:
        stmt = entries_table.select().where(entries_table.c.id == str(id))
        result = conn.execute(stmt).fetchone()
        if result:
            return Entry.from_db(*result)
        else:
            raise Exception("Entry not found")

def get_all_entries():
    with engine.begin() as conn:
        results = conn.execute(entries_table.select().order_by(entries_table.c.date.desc())).fetchall()
        return [Entry.from_db(*r) for r in results]

def update_entry(id: uuid.UUID, name: str, amount: float, category: str | None):
    with engine.begin() as conn:
        stmt = entries_table.update().where(entries_table.c.id == str(id)).values(
            name=name,
            amount=amount,
            category=category
        )
        conn.execute(stmt)

def delete_entry(id: uuid.UUID):
    with engine.begin() as conn:
        stmt = entries_table.delete().where(entries_table.c.id == str(id))
        conn.execute(stmt)
