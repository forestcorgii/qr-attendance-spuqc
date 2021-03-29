from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin



class Course(models.Model):
    name = models.CharField(max_length=100,blank=False,null=True)
    acronym = models.CharField(max_length=6, blank=False, null=True)
    
    def __str__(self):
        return self.acronym

class Location(models.Model):
    name = models.CharField(max_length=100,blank=False,null=True)

    def __str__(self):
        return self.name


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    id_number = models.CharField(max_length=25, null=True)
    
    first_name = models.CharField(max_length=100, blank=False,null=True)
    last_name = models.CharField(max_length=100, blank=False, null=True)
    middle_initial = models.CharField(max_length=2, blank=False, null=True)


    STUDENT=0
    OFFICE_SECRETARY=1
    HEAD=2
    ROLE_CHOICES = (
        (STUDENT, 'STUDENT'),
        (OFFICE_SECRETARY, 'OFFICE_SECRETARY'),
        (HEAD, 'HEAD'),
    )   
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=True)
        
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)



    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        permissions = (('office_secretary','Office Secretary'),('student','Student'))

    def fullname(self):
        return f"{self.last_name}, {self.first_name} {self.middle_initial}"

    def __str__(self):
        return self.fullname()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
