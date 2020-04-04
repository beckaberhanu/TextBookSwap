from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Manager

class Post(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)

    def validate_ISBN(self, value):
        if (len(value) != 10 or len(value) != 13):
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
    date_posted = models.DateTimeField(default=timezone.now)

    edition = models.PositiveSmallIntegerField(default=0)

    IN_PROGRESS = "In progress"
    COMPLETE = "Complete"
    states = (
        (IN_PROGRESS, "In progress"),
        (COMPLETE, "Complete"),
    )
    transaction_state = models.CharField(
        max_length=50, choices=states, default=IN_PROGRESS)

    objects=Manager()

    class Meta:
        verbose_name = 'Post'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Posts'
