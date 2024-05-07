import unittest
from app import app, db, Event, User
from datetime import datetime, timedelta

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_event_past_removal(self):
        with app.app_context():
            # Add a past event and a future event to the database
            past_event = Event(name='Past Event', time=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), description='This is a past event', user_id=1)
            future_event = Event(name='Future Event', time=(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), description='This is a future event', user_id=1)
            db.session.add(past_event)
            db.session.add(future_event)
            db.session.commit()

            # Make a request to the route for displaying events
            response = self.app.get('/dashboard')

            # Check that the past event is not in the response text
            self.assertNotIn('Past Event', response.get_data(as_text=True))

            # Check that the future event is in the response text
            self.assertIn('Future Event', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
