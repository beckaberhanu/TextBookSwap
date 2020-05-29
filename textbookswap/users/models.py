from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
# from tradeboard.models import Post
from PIL import Image


class Profile(models.Model):
    # 1-1 field pointing to correspoding user
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(
        default="default_profile.png", upload_to="profile_pics")  # saves image to a folder called ../media/profile_pics or references an image located at ../media/default_profile.png if left empty.

    def __str__(self):  # similar to a 'tostring' method in java
        return f"{self.user.username} Profile"

    class Meta:
        verbose_name = 'Profile'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Profiles'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(models.signals.post_delete, sender=Profile)
def submission_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Profile` object is deleted.
    """
    if not (instance.image.path == settings.MEDIA_ROOT + "/default_profile.png"):
        instance.image.delete(False)
    else:
        pass
    # more on how this works here https://stackoverflow.com/questions/16041232/django-delete-filefield
