from authentication.models import User
from .models import UserProfile, StaffProfile
from django.db.models.signals import post_save, post_delete


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance

        if user.is_staff == True:
            profile = StaffProfile.objects.create(
                user=user,
                email=user.email,
                name=user.name,
                empno=user.uid,
            )

        else:
            profile = UserProfile.objects.create(
                user=user,
                email=user.email,
                name=user.name,
                prn=user.uid,
            )


def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_user, sender=UserProfile)
post_delete.connect(delete_user, sender=StaffProfile)
