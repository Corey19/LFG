from django.test import TestCase
from django.urls import reverse  # To generate URLs
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from core.models import Tags, Games, Groups, Friends

class UserModelTest(TestCase):

    # Test for the user Model
    def setUp(self):
        self.User = get_user_model()
        self.username = "x" * 32
        self.password = "password123"
        self.email = "testuser@example.com"

    def test_creating_user(self):

        user1 = self.User.objects.create_user(username=self.username, password=self.password, email=self.email)

        self.assertEqual(user1, self.User.objects.get(username=self.username))

    def test_creating_username_len_error(self):
        username = "X" * 33  # Username exceeding max_length

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.User.objects.create_user(username=username, password=self.password, email=self.email)
         
        self.assertFalse(self.User.objects.filter(username=username).exists())

    def test_creating_user_dup_error(self):
        self.User.objects.create_user(username=self.username, password=self.password, email=self.email)
         
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.User.objects.create_user(username=self.username, password=self.password + '1', email="test@example.com")
                self.User.objects.create_user(username="test", password=self.password, email=self.email)
                 
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.User.objects.create_user(username="test", password=self.password, email=self.email)


class TagsModelTest(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="x", password="password123", email="testuser@example.com")
        
    def test_tags_create(self):
        tag1 = Tags(name='english')
        tag1.save()
        self.test_user.tags.add(tag1)

        tag2 = Tags(name='Spanish')
        tag2.save()
        self.test_user.tags.add(tag2)

        self.assertIn(tag1, self.test_user.tags.all())
        self.assertIn(tag2, self.test_user.tags.all())


class GamesModelTest(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="x", password="password123", email="testuser@example.com")
        
    def test_games_create(self):
        game1 = Games(name='Call of Duty')
        game1.save()
        self.test_user.games.add(game1)

        game2 = Games(name='Fortnite')
        game2.save()
        self.test_user.games.add(game2)

        self.assertIn(game1, self.test_user.games.all())
        self.assertIn(game2, self.test_user.games.all())


class GroupsModelTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="x1", password="password123", email="testuser1@example.com")
        self.user2 = get_user_model().objects.create_user(
            username="x2", password="password123", email="testuser2@example.com")
        self.user3 = get_user_model().objects.create_user(
            username="x3", password="password123", email="testuser3@example.com")
        
    def test_groups_create(self):
        group = Groups(name="group1")
        group.save()
        
        group.members.add(self.user1, self.user2, self.user3)

        self.assertIn(self.user1, group.members.all())
        self.assertIn(self.user2, group.members.all())
        self.assertIn(self.user3, group.members.all())


class FriendsModelTest(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="x1", password="password123", email="testuser1@example.com")
        self.user2 = get_user_model().objects.create_user(
            username="x2", password="password123", email="testuser2@example.com")
        self.user3 = get_user_model().objects.create_user(
            username="x3", password="password123", email="testuser3@example.com")
        
    def test_friends_create(self):
        friend1 = Friends(from_user=self.user1, to_user=self.user2)
        friend1.save()

        friend2 = Friends(from_user=self.user1, to_user=self.user3)
        friend2.save()

        all_frineds = Friends.objects.filter(from_user=self.user1)

        self.assertIn(self.user2.incoming_friends.all()[0], self.user1.outgoing_friends.all())
        self.assertIn(self.user3.incoming_friends.all()[0], self.user1.outgoing_friends.all())