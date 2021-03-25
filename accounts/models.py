from django.db import models

import jwt
from django.conf import settings

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from datetime import datetime
from django.utils.timezone import timedelta
import time
# Create your models here.



class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given  email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_teacher', False)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_teacher', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)
 
 

class TeacherManager(BaseUserManager):
    
    def get_queryset(self):
        return super(TeacherManager, self).get_queryset().filter(is_staff=False,is_teacher=True)

    def create_teacher(self,username ,first_name, last_name, email,  password=None, **extra_fields):
        
        if email is None:
            raise TypeError('Users must have an email address.')

        teacher = Teacher(username=username,first_name=first_name, last_name=last_name, 
                          email=self.normalize_email(email), is_teacher=True)
        
        teacher.set_password(password)
        teacher.save()
        return teacher
 
 


class StudentManager(BaseUserManager):
    
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(is_staff=False,is_teacher=False)

    def create_student(self,username, first_name, last_name, email,  password=None, **extra_fields):

        if email is None:
            raise TypeError('Users must have an email address.')
        
        student = Student(username=username,first_name=first_name, last_name=last_name, 
                            email=self.normalize_email(email),is_teacher=False)

        student.set_password(password)
        student.save()
        return student



class AdminUser(AbstractUser):
    username=models.CharField(blank=True,null=True,max_length=50)
    email = models.EmailField( unique=True)

    is_teacher = models.BooleanField(
        verbose_name='Teacher status',
        default=False,
        help_text='Designates whether the user is a teacher or not.',
    )
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','username']
    
    objects = UserManager()

    #generating token to be used by while authentication
    @property
    def token(self):
        dt = datetime.now() + timedelta(days=2)
        token = jwt.encode({
            'email': self.email,
            'exp': int(time.mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token


    def __str__(self):
        return self.email



class Teacher(AdminUser):
 
    objects = TeacherManager()
    class Meta:
        proxy =True
 
    def __str__(self):
        return self.first_name



class Student(AdminUser):

    objects = StudentManager()
    class Meta:
        proxy =True

    def __str__(self):
        return self.first_name


