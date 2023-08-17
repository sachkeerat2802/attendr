import uuid
from django.db import models
from authentication.models import User


class UserProfile(models.Model):
    choices = (
        ('BCA', 'BCA'),
        ('BBA-IT', 'BBA-IT'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    prn = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    course = models.CharField(max_length=10,
                              choices=choices, blank=True, null=True)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(
        upload_to='profiles/', default='profiles/default.jpeg', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.prn)


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    empno = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.IntegerField(null=True, blank=True)
    image = models.ImageField(
        upload_to='profiles/', default='profiles/default.jpeg', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.empno)
