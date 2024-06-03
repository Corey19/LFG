from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .forms import MyUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.test import Client

class CreateUserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('user:create_user') # Replace 'create_user' with your actual URL pattern name
        self.creation_form = MyUserCreationForm

    def test_get_renders_registration_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
        form = response.context['form']
        self.assertIsInstance(form, MyUserCreationForm)  # Or MyUserCreationForm if it's a custom form

    def test_post_with_valid_data_creates_user(self):
        valid_data = {
            'username': 'valid_user',
            'email':'invalidEmail@example.com', 
            'password1': 'strong_password',
            'password2': 'strong_password',
            # Add other fields as needed based on your MyUserCreationForm
        }
        response = self.client.post(self.url, valid_data)

        self.assertEqual(response.status_code, 302)  # Redirect to login page (or another URL)
        self.assertEqual(get_user_model().objects.count(), 1)
        user = get_user_model().objects.get(username=valid_data['username'])
        self.assertTrue(user.is_active)  # Ensure user is active by default

    def test_post_with_invalid_data(self):
        invalid_data = {'username': 'x' * 33,
                        'email':'invalidEmail@example.com', 
                        'password1': 'weak_password',
                        'password2': 'weak_password'}
        response = self.client.post(self.url, invalid_data)
        form = self.creation_form(invalid_data)

        self.assertEqual(response.status_code, 200)  # Renders the registration form with errors
        self.assertTemplateUsed(response, 'user/register.html')
        self.assertFalse(form.is_valid())  # Check for form validation errors in the context


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('user:login_user')  # Replace 'login' with your actual URL pattern name
        self.user = get_user_model().objects.create_user(username='valid_user', password='valid_password@123', email='testuser@example.com')

    def test_get_renders_login_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        form = response.context['form']
        self.assertIsInstance(form, AuthenticationForm)

    def test_post_with_valid_credentials_redirects(self):
        valid_data = {
            'username': 'valid_user',
            'password': 'valid_password@123',
        }
        response = self.client.post(self.url, valid_data)

        self.assertRedirects(response, expected_url=None)  # Redirect URL might vary
        # Optional: Assert user is logged in using request.user

    def test_post_with_invalid_credentials(self):
        invalid_data = {'username': 'invalid_user', 'password': 'wrong_password'}
        response = self.client.post(self.url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')
        self.assertFalse(AuthenticationForm(invalid_data).is_valid()) 


    class LogoutViewTest(TestCase):

        def setUp(self):
            self.client = Client()
            self.url = reverse('user:login_user')  # Replace 'user:login_user' with your actual URL pattern name
            self.user = get_user_model().objects.create_user('valid_user', 'valid_password@123', is_active=True)
            self.client.login(username='valid_user', password='valid_password@123')  # Log in the user

        def test_get_redirects_to_login_if_authenticated(self):
            response = self.client.get(self.url)

            self.assertRedirects(response, reversed("user:login_user"))  # Redirect URL might vary
            self.assertFalse(self.client.session.has_key('_auth_user_id'))  # Verify user is logged out
