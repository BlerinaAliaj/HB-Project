""" Write Unit Tests:

1. Test Home page - done
2. Test Login page - done
3. Test Registration page
4. Test Logout Page - done
5. Test Profile
6. Test New Trip page
7. Test Trip Detail page
8. Test List page

"""
import unittest
# from unittest import TestCase
from server import app
from model import User, db, connect_to_db
from flask import session


class FlaskTests(unittest.TestCase):
    """Tests for Hiker app """

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app)

    def test_homepage(self):
        """Tests homepage.html """

        result = self.client.get("/")
        self.assertIn("Welcome to the One-Stop Location for adventure planning", result.data)
        self.assertIn("Login", result.data)

    def test_no_login(self):
        """Tests that user has not loged in yet"""

        result = self.client.get("/")
        self.assertIn("Let's start", result.data)
        self.assertIn("Login", result.data)
        self.assertIn("Register", result.data)
        self.assertNotIn("Member Home Page", result.data)

    def test_login_page(self):
        """Tests login page"""

        result = self.client.get("/login")
        self.assertIn("User Login", result.data)
        self.assertIn("User Name", result.data)
        self.assertIn("Password", result.data)
        self.assertIn("Submit", result.data)
        self.assertNotIn("Logout", result.data)
        self.assertNotIn("Member Home Page", result.data)

    def test_login(self):
        """ Tests login procedure"""

        with self.client as c:

            result = c.post("/login", data={'username': "baliaj",
                            "password": "blerina"}, follow_redirects=True)

            self.assertEqual(session['user'], 'baliaj')
            self.assertIn("Hello Blerina", result.data)
            self.assertIn("You have successfully logged in.", result.data)
            self.assertIn("Create New Trip", result.data)
            self.assertIn("This is a list of your most recent trips:", result.data)
            self.assertIn("Member Home Page", result.data)
            self.assertIn("Logout", result.data)

    def test_registration(self):
        """Tests registration page"""

        result = self.client.get("/register")
        self.assertIn("User Name", result.data)
        self.assertIn("First Name", result.data)
        self.assertIn("Last Name", result.data)
        self.assertIn("Email", result.data)
        self.assertIn("Password", result.data)
        self.assertIn("Zip Code", result.data)
        self.assertNotIn("Member Home Page", result.data)
        self.assertNotIn("Logout", result.data)

    def test_profile(self):

        result = self.client.get('/profile')
        self.assertIn("Redirecting", result.data)
        # self.assertIn("Register", result.data)
        # self.assertNotIn("Member Home Page", result.data)

        # self.assertIn("This is a list of your most recent trips:", result.data)

    def test_logout(self):
        """Tests logout procedure"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 'baliaj'
            
            result = self.client.get("/logout", follow_redirects=True)
            self.assertNotIn('user', session)
            self.assertIn("You have been successfully logged out.", result.data)
            self.assertNotIn("Member Home Page", result.data)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
