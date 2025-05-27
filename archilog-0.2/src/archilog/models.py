from sqlalchemy import *
#import sqlite3
import uuid

from dataclasses import dataclass


db_url = "sqlite:///data.db"
engine = create_engine(db_url, echo=True)
metadata = MetaData()


entries_table = Table(
    "entries",
    metadata,
    Column("id", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("amount", Float, nullable=False),
    Column("category", String, nullable=True),
)



def init_db():
    metadata.create_all(engine)



@dataclass
class Entry:
    id: uuid.UUID
    name: str
    amount: float
    category: str | None

    @classmethod
    def from_db(cls, id: str, name: str, amount: float, category: str | None):
        return cls(
            uuid.UUID(id),
            name,
            amount,
            category,
        )


def create_entry(name: str, amount: float, category: str | None = None):
    with engine.begin() as conn:
        conn.execute(
            entries_table.insert().values(
                id=uuid.uuid4().hex,
                name=name,
                amount=amount,
                category=category
            )
        )



def get_entry(id: uuid.UUID):
    with engine.begin() as conn:
        stmt = entries_table.select().where(entries_table.c.id == id.hex)
        result = conn.execute(stmt).fetchone()
        if result:
            return Entry.from_db(*result)
        else:
            raise Exception("Entry not found")



def get_all_entries():
    with engine.begin() as conn:
        results = conn.execute(entries_table.select()).fetchall()
        return [Entry.from_db(*r) for r in results]



def update_entry(id: uuid.UUID, name: str, amount: float, category: str | None):
    with engine.begin() as conn:
        stmt = entries_table.update().where(entries_table.c.id == id.hex).values(
            name=name,
            amount=amount,
            category=category
        )
        conn.execute(stmt)



def delete_entry(id: uuid.UUID):
    with engine.begin() as conn:
        stmt = entries_table.delete().where(entries_table.c.id == id.hex)
        conn.execute(stmt)

