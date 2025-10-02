###
# Testing setup - the database URL used must point to an empty db to start
###
import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import any_table_exist
from db.manage import load_data, create_tables


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """The testing database must start empty"""
    # in bigger applications it may not be feasible to load all sample data before each test session,
    # in that case dedicated testing db's should be created

    # allows use of a non in memory sqlite database because it might be useful to manually inspect the state of it after testing

    if any_table_exist():
        raise ValueError("Database is not empty, use an empty database for testing")

    create_tables()
    load_data()


@pytest.fixture(scope="function")
def test_client():
    """This testclient will use the in-memory SQLite database."""

    yield TestClient(app)

    # Clean up the dependency override after the test
    app.dependency_overrides.clear()
