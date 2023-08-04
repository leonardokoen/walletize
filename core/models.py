from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your CustomUserManager here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, phone_number, vat_number, date_of_birth, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')
        if not first_name:
            raise ValueError('First Name must be provided')
        if not last_name:
            raise ValueError('Last Name must be provided')
        if not phone_number:
            raise ValueError('Phone Number must be provided')
        if not vat_number:
            raise ValueError('Vat Number must be provided')
        if not date_of_birth:
            raise ValueError('Date of Birth must be provided')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
            vat_number = vat_number,
            date_of_birth = date_of_birth,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, phone_number, vat_number, date_of_birth, **extra_fields):
        extra_fields.setdefault('is_active',False)
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, first_name, last_name, phone_number, vat_number, date_of_birth, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, phone_number, vat_number, date_of_birth, **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_staff',True)
        return self._create_user(email, password, first_name, last_name, phone_number, vat_number, date_of_birth, **extra_fields)

# Create your User Model here.
class User(AbstractBaseUser,PermissionsMixin):
    # Abstractbaseuser has password, last_login, is_active by default

    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    vat_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()

    is_staff = models.BooleanField(default=True) # must needed, otherwise you won't be able to loginto django-admin.
    is_active = models.BooleanField(default=False) # must needed, otherwise you won't be able to loginto django-admin.
    is_superuser = models.BooleanField(default=False) # this field we inherit from PermissionsMixin.
    # address = models.CharField( max_length=250)

    # must needed, otherwise you won't be able to loginto django-admin.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number', 'password', 'vat_number', 'date_of_birth']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'