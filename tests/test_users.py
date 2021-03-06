# tests/test_users.py


import unittest

from flask_login import current_user
from flask import request

from base import BaseTestCase
from mvm import bcrypt
from mvm.models import User


class TestUser(BaseTestCase):

    # Ensure user can register
    def test_user_registration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='maxmustermann', email='max@mustermann.com',
                password='mm@mvm', confirm_password='mm@mvm'
            ), follow_redirects=True)            
            self.assertIn(b'Your account has been created! you are able to log in', response.data)
            self.assertFalse(current_user.is_active)
            user = User.query.filter_by(email='max@mustermann.com').first()
            self.assertTrue(str(user) == "User('maxmustermann', 'max@mustermann.com', 'default.jpg')")

    # Ensure user can register
    def test_user_registration_and_login(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='maxmustermann1', email='max1@mustermann.com',
                password='mm@mvm', confirm_password='mm@mvm'
            ), follow_redirects=True)            
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="max1@mustermann.com", password="mm@mvm"),
                follow_redirects=True
            )
            self.assertTrue(current_user.username == "maxmustermann1")
            self.assertTrue(current_user.is_active)

    # Ensure errors are thrown during an incorrect user registration
    def test_incorrect_user_registeration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='Michael', email='michael',
                password='python', confirm_password='python'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address', response.data)
            self.assertIn('/register', request.url)

    # Ensure id is correct for the current/logged in user
    def test_get_by_id(self):
        with self.client:
            response = self.client.post('/login', data=dict(
                email="ad@min.com", password='admin'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    # Ensure given password is correct after unhashing
    def test_check_password(self):
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))


class UserViewsTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Log In', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin"),
                follow_redirects=True
            )
#            self.assertIn(b'You were logged in', response.data)
            self.assertTrue(current_user.username == "admin")
            self.assertTrue(current_user.is_active)

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(email="wro@ng.com", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Login Unsuccessful. Please check email and password', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="ad@min.com", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'MVM', response.data)
            self.assertFalse(current_user.is_active)


if __name__ == '__main__':
    unittest.main()
