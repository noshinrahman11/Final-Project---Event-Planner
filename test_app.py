import pytest
from app import app, db, User

# This is messing with my database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_signup(client):
    response = client.get('/signup')
    assert response.status_code == 200

# Redirects (302) to index if the user is not logged in
def test_dashboard(client):
    response = client.get('/dashboard')
    assert response.status_code == 302

if __name__ == '__main__':
    pytest.main()
