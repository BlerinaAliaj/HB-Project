""" Write Unit Tests:

1. Test Home page
2. Test Login page
3. Test Registration page
4. Test Logout Page
5. Test Profile
6. Test New Trip page
7. Test Trip Detail page
8. Test List page

"""

from unittest import TestCase
from server import app


class FlaskTests(TestCase):
    """Tests for Hiker app """

    def setUp(self):

        self.client = app.test_client()
        app.config['Testing'] = True

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

    def test_login(self):
        """Tests login page"""

        result = self.client.get("/login")
        self.assertIn("User Login", result.data)
        self.assertIn("User Name", result.data)
        self.assertIn("Password", result.data)
        self.assertIn("Submit", result.data)
        self.assertNotIn("Logout", result.data)
        self.assertNotIn("Member Home Page", result.data)

    def test_logout(self):
        """Tests logout page"""

        result = self.client.get("/")
        self.assertIn("You have successfully logged out", result.data)
        self.assertNotIn("Member Home Page", result.data)

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
        


    def tearDown(self):
        pass
