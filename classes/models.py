import uuid
from django.db import models
from users.models import StaffProfile, UserProfile


class Class(models.Model):
    name = models.CharField(max_length=100)
    profile = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='classes/', default='classes/default.png', blank=True, null=True)
    users = models.ManyToManyField(UserProfile)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    class_object = models.ForeignKey(Class, on_delete=models.CASCADE)
    no = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.no)


class Attendance(models.Model):
    choices = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )

    class_object = models.ForeignKey(
        Class, on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    value = models.CharField(max_length=10,
                             choices=choices, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value)
