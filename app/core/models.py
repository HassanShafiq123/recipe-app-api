from django.db import models
from django.contrib.auth.models import (
                                        AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extraFields):
        """ CREATE AND SAVE'S A NEW USER """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extraFields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """CREATE AND SAVE'S A NEW SUPERUSER"""
        if not email:
            raise ValueError('Superuser must have an email address')
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ CUSTOM USER MODEL THAT SUPPORTS EMAIL INSTEAD OF USERNAME """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
