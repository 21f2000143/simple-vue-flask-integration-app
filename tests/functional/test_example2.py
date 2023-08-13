from main import app
import pytest
from application.database import db

@pytest.fixture()
def client():
    ## Arrange
    print("SETTING UP CLIENT")
    client =app.test_client()
    ctx = app.app_context()
    ctx.push()

    #Act
    yield client

    #Cleanup
    print('CLEANING UP CLIENT')
    ctx.pop()

@pytest.fixture()
def init_database():
    print("SETTING UP DATABASE")
    # create the database and database table
    db.create_all()

    yield db # this where the testing happens

    #Tear down
    print("CLEANING UP DB")
    db.drop_all()

def test_no_articles_home(client, init_database):
    print("RUNNING")
    ## Act
    response = client.get('/')
    ## Assert
    assert b"<title>Ticket Show</title>" in response.data