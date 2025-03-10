from main import app
from application.database import db

def test_no_articles_home():
    ## Arranging
    client =app.test_client()
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    ## Act
    response = client.get('/')
    ## Assert
    assert b"<title>Ticket Show</title>" in response.data

    ## Cleanup
    ctx.pop()
    db.drop_all()