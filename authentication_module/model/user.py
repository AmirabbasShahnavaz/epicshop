from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=400,unique=True, null=True)
    mobile_verify_code = models.PositiveIntegerField(null=True,blank=True, unique=True)
    forgot_password_verify_code = models.PositiveIntegerField(null=True,blank=True, unique=True)
    otp_verify_code = models.PositiveIntegerField(null=True,blank=True, unique=True)
    email_verify_code = models.CharField(max_length=450, null=True,blank=True, unique=True)
    is_email_active = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/',null=True,blank=True)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.mobile

    def get_header_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'سلام  09xxxxxx{self.mobile[9:12]}'

    def is_full_name(self):
        if self.first_name and self.last_name:
            return True
        return False