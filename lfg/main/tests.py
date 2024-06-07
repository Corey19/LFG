from django.test import TestCase
from django.urls import reverse  # To generate URLs
from django.contrib.auth import get_user_model, authenticate
from django.db import IntegrityError, transaction
from core.models import Tags, Games, Groups, Friends
from django.test import Client
from .forms import CreateGroupForm
from django.db.models.query import QuerySet

class ExploreViewTests(TestCase):

    def setUp(self):
        self.password = "testing123!"
        self.user = get_user_model().objects.create_user(username="test_user", email="test@example.com", password=self.password)
        self.client = Client()
        self.games = Games.objects.create(name="Test Game 1"), Games.objects.create(name="Test Game 2")

    def test_get_request_authenticated(self):
        # Simulate a logged-in user
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.get(reverse("main:explore"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/explore.html')
        self.assertContains(response, 'Test Game 1')
        self.assertContains(response, 'Test Game 2')

    def test_get_request_not_authenticated(self):
        response = self.client.get(reverse("main:explore"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, '/login/?next=' + reverse("main:explore"))

    def test_post_request_not_authenticated(self):
        response = self.client.post(reverse("main:explore"))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, '/login/?next=' + reverse("main:explore"))


class CreateGroupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.email = "test@example.com"
        self.password = "TEStpassword12!"
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.game = Games(name="call of duty")
        self.game.save()

    def test_get_request_authenticated(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('main:create_group')  # Use reverse to get the URL by name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_group.html')
        self.assertIsInstance(response.context['form'], CreateGroupForm)

    def test_get_request_not_authenticated(self):
        url = reverse('main:create_group')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, '/login/?next=' + reverse("main:create_group"))

    def test_post_request_authenticated_valid_form(self):
        self.client.login(username=self.username, password=self.password)

        data = {'name': 'Test Group',
                'game': self.game.pk,
                'group_size': 5,
                'is_public': False,}
        url = reverse('main:create_group')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Redirect to explore page
        self.assertRedirects(response, reverse("main:explore"))

        # Check if the group was created
        group = Groups.objects.get(name='Test Group')
        self.assertTrue(self.user in group.members.all())

    def test_post_request_authenticated_invalid_form(self):
        self.client.login(username=self.username, password=self.password)

        data = {}  # Empty data, form will be invalid
        url = reverse('main:create_group')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_group.html')
        self.assertIsInstance(response.context['form'], CreateGroupForm)

    def test_post_request_not_authenticated(self):
        data = {'name': 'Test Group'}
        url = reverse('main:create_group')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, '/login/?next=' + reverse("main:create_group"))


class FindGroupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.email = "test@example.com"
        self.password = "TEStpassword12!"
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)

    def test_get_request_authenticated(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('main:find_group') 
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/find_group.html')
        self.assertIsInstance(response.context['groups'], QuerySet)


class JoinGroupViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.username = "test_user"
        self.email = "test@example.com"
        self.password = "TEStpassword12!"
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.group = Groups(name='Test Group')
        self.group.save()
    
    

    def test_post_request_authenticated_valid_group(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('main:join_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Redirect to find_group page
        self.assertRedirects(response, reverse('main:find_group'))

        # Check if the user is now a member of the group
        self.assertTrue(self.user in self.group.members.all())

    def test_post_request_authenticated_invalid_group(self):
        self.client.login(username=self.username, password=self.password)

        # Group with a non-existent ID
        invalid_id = 1000  # Assuming no group with this ID exists
        url = reverse('main:join_group', kwargs={'group_id': invalid_id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Redirect to find_group page (expected behavior)
        self.assertRedirects(response, reverse('main:find_group'))

        # User should not be added to any group
        self.assertFalse(self.user in self.group.members.all())

    def test_post_request_not_authenticated(self):
        url = reverse('main:join_group', kwargs={'group_id': self.group.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertRedirects(response, '/login/?next=' + reverse("main:join_group", kwargs={'group_id': self.group.pk}))


class GroupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = "test_user"
        self.email = "test@example.com"
        self.password = "TEStpassword12!"
        self.user = get_user_model().objects.create_user(username=self.username, email=self.email, password=self.password)
        self.group = Groups.objects.create(name='Test Group')
        self.group.members.add(self.user)  # Add user to the group

    def test_get_request_authenticated_member(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('main:group', kwargs={'group_id': self.group.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)  # Successful response
        self.assertTemplateUsed(response, 'main/group.html')  # Verify template used
        self.assertContains(response, self.group.name)  # Check group name in context

    def test_get_request_not_authenticated(self):
        url = reverse('main:group', kwargs={'group_id': self.group.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/login/?next=' + reverse('main:group', kwargs={'group_id': self.group.pk}))

    def test_get_request_not_member(self):
        # Create another user who is not a member
        another_user = get_user_model().objects.create_user(username=self.username + '1', email="test2@example.com", password=self.password)
        self.client.login(username=self.username + '1', password=self.password)

        url = reverse('main:group', kwargs={'group_id': self.group.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)  # Redirect to find_group
        self.assertRedirects(response, reverse('main:find_group'))