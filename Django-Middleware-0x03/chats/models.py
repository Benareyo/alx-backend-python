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
