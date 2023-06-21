import unittest
from app import app, db, User, Post

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Home Page', response.data)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_dashboard_page(self):
        # Create a test user
        user = User(name='Test User', email='test@example.com', password='test')
        db.session.add(user)
        db.session.commit()

        # Login as the test user
        with self.client.session_transaction() as session:
            session['user_id'] = user.id

        # Test dashboard page with no filter
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

        # Test dashboard page with filter
        response = self.client.post('/dashboard', data=dict(filter_text='test'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test User', response.data)

    def test_api_all_posts(self):
        # Create test posts
        post1 = Post(title='Post 1', content='Test content 1', upvotes=10, comment_count=5)
        post2 = Post(title='Post 2', content='Test content 2', upvotes=20, comment_count=10)
        db.session.add_all([post1, post2])
        db.session.commit()

        # Test API endpoint
        response = self.client.get('/api/allposts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)
        self.assertIn(b'Post 2', response.data)

if __name__ == '__main__':
    unittest.main()

# I can't pass all the tests, unfortunately, can we solve it together?