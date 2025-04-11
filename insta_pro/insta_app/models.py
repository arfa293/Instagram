from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
 
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,email,username,password,**extra_fields):
        if not email:
            raise ValueError('Email is required')
        email=self.normalize_email(email)
        user=self.model(email=email,username=username, password=password,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields) 
    
class CustomUser(AbstractBaseUser):
    username=models.CharField(max_length=100 ,unique=True)
    email=models.EmailField(unique=True)
    profile_picture=models.ImageField(upload_to='profile_pics/',null=True,blank=True)
    bio=models.TextField(max_length=100 ,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False) 

    objects=CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Post(models.Model):
    author=models.ForeignKey(CustomUser, on_delete=models.CASCADE , related_name='posts')
    caption=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='post_images', null=False)

    def __str__(self):
        return self.caption