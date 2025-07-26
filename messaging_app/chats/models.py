<<<<<<< HEAD
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
import uuid 
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy  as _


# The CustomUserManager class is added by myself to authenticate by email instead of username
class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is used instead of username
    as the unique identifier for authentication.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        # Set required flags for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Validate flags
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    class UserRole(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'
    user_id  = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False,
                            db_index=True)
    email  =models.EmailField(unique=True,null=False)
    phone_number  =models.CharField(max_length=255,null=True)
    role=models.CharField(max_length=15,choices=UserRole.choices,null=False)
    created_at=models.DateTimeField(auto_now_add=True)

    username = None  # Disable username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['first_name','last_name']
    #add the base CustomUserManager
    objects = CustomUserManager()
    def __str__(self):
            return f"{self.email}"

class Conversation(models.Model):
    conversation_id =models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False,
                            db_index=True)
    participants =models.ManyToManyField(User,related_name='conversations')
    created_at=models.DateTimeField(auto_now_add=True)
       
    def __str__(self):
          return f"Conversation {self.conversation_id}"
class Message(models.Model):
    message_id=models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False,
                            db_index=True)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    conversation = models.ForeignKey(
    Conversation,
    on_delete=models.CASCADE,
    related_name='messages',
    null=True,       # Allow null temporarily
    blank=True       # Allow blank in forms/admin (optional)
)

    # conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body=models.TextField(null=False)
    sent_at=models.DateTimeField(auto_now_add=True)
       
    def __str__(self):
          return f"Message {self.message_id} from {self.sender.email}"
=======
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128, null=False)  # password hash
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='chats_user_set',  # Unique related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='chats_user_set',  # Unique related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.conversation_id)


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        null=False,
        default=1  
    )
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:20]}"
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
