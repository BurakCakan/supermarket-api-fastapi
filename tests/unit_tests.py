import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database import (
    insert_team,
    delete_team,
    delete_team_member,
    get_products,
    team,
)

@pytest.fixture(scope="module")
def db():

    #please complete </> parts below like your postgres credentials
    engine = create_engine("postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@<POSTGRES_HOST_IP>:5432/perishable_foods")
    conn = engine.connect()
    transaction = conn.begin()
    yield conn
    transaction.rollback()
    conn.close()

@pytest.fixture(scope="function")
def session(db):

    session = Session(bind=db)
    yield session
    session.rollback()
    session.close()

def test_insert_team(session):

    insert_team("Team A", "http://example.com", "abc123")
    result = session.query(team).filter_by(name="Team A").one()
    assert result.endpoint == "http://example.com"
    assert result.api_key == "abc123"

def test_delete_team(session):

    insert_team("Team A", "http://example.com", "abc123")
    delete_team("Team A")
    assert session.query(team).filter_by(name="Team A").count() == 0

def test_delete_team_member(session):

    insert_team("Team A", "http://example.com", "abc123")
    result = session.query(team).filter_by(name="Team A").one()
    team_id = result.team_id
    delete_team_member(team_id)
    assert session.query(team).filter_by(team_id=team_id).count() == 0

def test_get_products(session):
    
    response = get_products()
    assert isinstance(response, dict)
