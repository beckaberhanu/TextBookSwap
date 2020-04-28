from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Manager

# link for a good video on creating custom html forms: https://www.youtube.com/watch?v=9jDEnSm4nt8


class Post(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)

    def validate_ISBN(value):
        print(not(f'{value}'.isnumeric()))
        if (len(value) != 10 and len(value) != 13):
            raise ValidationError(f'number of digits in {value} is neither 10 nor 13',
                                  params={'value': value},
                                  )
        elif (not(f'{value}'.isnumeric())):
            raise ValidationError(f'{value} has non-numeric elements',
                                  params={'value': value},
                                  )

    ISBN = models.CharField(max_length=13, validators=[validate_ISBN])

    author = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    image = models.ImageField(
        default='default_book.png', upload_to='book_pics')
    date_posted = models.DateTimeField(default=timezone.now)  # UTC time

    edition = models.PositiveSmallIntegerField(blank=True, null=True)

    price = models.PositiveSmallIntegerField(default=0)
    swappable = models.BooleanField(default=False)

    # ****************************************************************************************
    IN_PROGRESS = "In progress"
    COMPLETE = "Complete"
    states = (
        (IN_PROGRESS, "In progress"),
        (COMPLETE, "Complete"),
    )
    transaction_state = models.CharField(
        max_length=50, choices=states, default=IN_PROGRESS)
    # ****************************************************************************************
    OTHER = "Other"
    TEXTBOOK = "Textbook"
    post_types = (
        (OTHER, "Other"),
        (TEXTBOOK, "Textbook"),
    )
    post_type = models.CharField(
        max_length=50, choices=post_types, default=OTHER)
    # ****************************************************************************************

    objects = Manager()

    def __str__(self):
        return(f"Post| Seller: {self.seller} | Title: {self.title} | ID: {self.pk}")

    class Meta:
        verbose_name = 'Post'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Posts'


@receiver(models.signals.post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    """
    Deletes image from filesystem
    when corresponding `Post` object is deleted.
    """
    if not (instance.image.path == settings.MEDIA_ROOT + "/default_book.png"):
        instance.image.delete(False)
    else:
        pass
    # more on how this works here https://stackoverflow.com/questions/16041232/django-delete-filefield
