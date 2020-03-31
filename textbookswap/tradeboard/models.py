from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    ISBN = models.CharField(max_length=13)

    author = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    image = models.ImageField(
        default='default_book.png', upload_to='book_pics')
    date_posted = models.DateTimeField(default=timezone.now)

    IN_PROGRESS = "in progress"
    COMPLETE = "complete"
    states = (
        (IN_PROGRESS, "in progress"),
        (COMPLETE, "complete"),
    )
    transaction_state = models.CharField(
        max_length=50, choices=states, default=IN_PROGRESS)
