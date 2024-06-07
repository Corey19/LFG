from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator


class Tags(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Games(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class MyUserManager(UserManager):
    def create_user(self, email, password, username, **extra_fields):
        if not email and username:
            raise ValueError("The Email and Username must be set")
        elif len(username) > 32:
            raise IntegrityError("username cant be longer than 32 characters")
        email = self.normalize_email(email)
        user = self.model(email=email,
                          username=username,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    tags = models.ManyToManyField(Tags, related_name='user_tags', blank=True)
    games = models.ManyToManyField(Games, related_name='user_games', blank=True)
   
    objects = MyUserManager()
   
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Groups(models.Model):
    name = models.CharField(max_length=255, unique=False)
    members = models.ManyToManyField(User, related_name='user_groups')
    group_size = models.IntegerField(default=6, validators=[MinValueValidator(1), MaxValueValidator(6)])
    is_public = models.BooleanField(default=True)
    game = models.ForeignKey(Games, default=None, null=True, blank=True, on_delete=models.CASCADE) 



class Friends(models.Model):
    from_user = models.ForeignKey(User, related_name='outgoing_friends', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='incoming_friends', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('from_user', 'to_user')]