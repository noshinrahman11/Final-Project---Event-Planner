import pytest
from app import app, db, User

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

def test_dashboard(client):
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_new_user():
    user = User('noshin@gmail.com', 'noshin', 'password')
    assert user.email == 'noshin@gmail.com'
    assert user.hashed_password != 'Password!1'
    assert user.role == 'user'


if __name__ == '__main__':
    pytest.main()
