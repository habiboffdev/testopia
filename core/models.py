import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    Custom manager for our custom user model.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class BaseManager(models.Manager):
    """
    Our basic manager is used to order all child models of BaseLayer
    to be ordered by created time (descending), therefore it creates a LIFO order,
    causing the recent ones appear first in results.
    """
    use_for_related_fields = True

    def get_queryset(self):
        return super(BaseManager, self).get_queryset().order_by('-created_time')

class BaseLayer(models.Model):
    """
    This layer makes system-wide configurations which tend to be effective for every single model.
    It is used as a parent class for all other models.
    """

    # let's configure managers
    default_manager = BaseManager
    objects = BaseManager()
    all_objects = models.Manager()

    # all models are going to have following two fields
    created_time = models.DateTimeField(default=timezone.now)
    last_updated_time = models.DateTimeField(default=timezone.now)

    @classmethod
    def create(cls, *args, **kwargs):
        now = timezone.now()
        obj = cls(
            *args,
            **kwargs,
            created_time=now,
            last_updated_time=now
        )
        obj.save()
        return obj

    def save(self, *args, **kwargs):
        self.last_updated_time = timezone.now()
        return super(BaseLayer, self).save(*args, **kwargs)

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return cls.objects.get(*args, **kwargs)
        except cls.DoesNotExist:
            return None

    @classmethod
    def all(cls, *args, **kwargs):
        return cls.objects.all()

    @classmethod
    def filter(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, BaseLayer):
    """
    To store users
    """
    CHOICES = [(0, "telegram"), (1, "website")]
    uid = models.IntegerField(unique=True,null=True,blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    rating = models.BigIntegerField(default=0)
    full_name = models.TextField(null=True, blank=True)
    username = models.CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers and underscores', code=False)]
    )
    platform = models.CharField(max_length=2, choices=CHOICES, default=0)
    step = models.IntegerField(blank=True, null=True, default=0)
    temp_data = models.TextField(null=True, blank=True)
    magic_word = models.CharField(max_length=63, null=True, blank=True)
    welcome_message_id = models.IntegerField(null=True, blank=True)
    agreement_time = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)  # Assuming you may want to use email as well
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.full_name or ''} {self.uid}".lstrip()

    class Meta:
        db_table = 'users'
