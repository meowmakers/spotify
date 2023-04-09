from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager 

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('введите username')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user 
    
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_contant_maker', False)
        return self._create(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_contant_maker', False)
        return self._create(username, email, password, **extra_fields) 
    

class CustomUser(AbstractBaseUser):
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_contant_maker = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)
    
    REQUIRED_FIELDS = ['email']
    
    USERNAME_FIELD = 'username'
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    def has_perm(self, obj=None):
        return self.is_staff
    
    objects = CustomUserManager()

    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'