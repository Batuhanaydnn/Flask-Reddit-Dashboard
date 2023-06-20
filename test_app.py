import pytest
from app import app, db, User, Post

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register(client):
    response = client.post('/register', data=dict(
        name='Test User',
        email='testuser@example.com',
        password='testpassword'
    ), follow_redirects=True)
    assert b'Login' in response.data

def test_login(client):
    user = User(name='Test User', email='testuser@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()
    response = client.post('/login', data=dict(
        email='testuser@example.com',
        password='testpassword'
    ), follow_redirects=True)
    assert b'Dashboard' in response.data

def test_dashboard(client):
    user = User(name='Test User', email='testuser@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()
    response = client.get('/dashboard', follow_redirects=True)
    assert b'Login' in response.data
    client.post('/login', data=dict(
        email='testuser@example.com',
        password='testpassword'
    ), follow_redirects=True)
    response = client.get('/dashboard')
    assert b'Test User' in response.data

def test_api_posts(client):
    user = User(name='Test User', email='testuser@example.com', password='testpassword')
    db.session.add(user)
    db.session.commit()
    post = Post(title='Test Post', content='This is a test post', user=user)
    db.session.add(post)
    db.session.commit()
    response = client.get('/api/posts/')
    assert response.json['posts'][0]['title'] == 'Test Post'

