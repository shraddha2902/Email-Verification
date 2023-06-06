from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    uid=models.OneToOneField(User,on_delete=models.CASCADE,db_column='uid')
    mobile=models.CharField(unique=True,max_length=50)
    is_mobile_verified=models.BooleanField(default=False)
    is_gmail_verified=models.BooleanField(default=False)
    mobileotp=models.CharField(max_length=100,default=False)
    gmailotp=models.CharField(max_length=100,default=False)