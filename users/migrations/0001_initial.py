# Generated by Django 4.0.6 on 2023-02-14 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('prn', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('course', models.CharField(blank=True, choices=[('BCA', 'BCA'), ('BBA-IT', 'BBA-IT')], max_length=10, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='profiles/default.png', null=True, upload_to='profiles/')),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('empno', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='profiles/default.png', null=True, upload_to='profiles/')),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
