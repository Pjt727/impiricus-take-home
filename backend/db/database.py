#####
# Setup sqlalchemy database
#####


from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
import os


DB_URL = os.environ.get("DB_URL", "sqlite:///impiricus.db")

# for tests to work in memory sqlite datbase needs to be able to run on different threads
if DB_URL == "sqlite:///:memory:":
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(DB_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)


def any_table_exist() -> bool:
    inspector = inspect(engine)

    return len(inspector.get_table_names()) > 0
