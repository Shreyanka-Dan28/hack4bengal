from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError('User should have a username')
        if email is None:
            raise TypeError('User should have a email')
        
        user=self.model(username=username,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,password):
        if password is None:
            raise TypeError('User should have a password')
        
        user=self.create_user(username,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user
    

AUTH_PROVIERS={'facebook':'facebook','google':'google','email':'email'}
class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=255,unique=True,db_index=True)
    email=models.EmailField(max_length=255,unique=True,db_index=True)
    is_verified=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    auth_provider=models.CharField(max_length=255,blank=False,null=False,default=AUTH_PROVIERS.get('email'))

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    objects=UserManager()

    def __str__(self):
        return self.username
    #def __str__(self) -> str:
    #    return self.email
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }


