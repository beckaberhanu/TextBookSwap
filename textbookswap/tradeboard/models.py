from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Manager

# link for a good video on creating custom html forms: https://www.youtube.com/watch?v=9jDEnSm4nt8


class Post(models.Model):
    # ****************************************************************************************
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=False, related_name="posts")
    # ****************************************************************************************
    title = models.CharField(max_length=100)
    # ****************************************************************************************

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
    # ****************************************************************************************
    author = models.CharField(max_length=50)
    # ****************************************************************************************
    description = models.TextField(max_length=350)
    # ****************************************************************************************
    image = models.ImageField(
        default='default_book.png', upload_to='book_pics')
    # ****************************************************************************************
    date_posted = models.DateTimeField(default=timezone.now)  # UTC time
    # ****************************************************************************************
    edition = models.PositiveSmallIntegerField(blank=True, null=True)

    # ****************************************************************************************
    price = models.PositiveSmallIntegerField(default=0)

    # ****************************************************************************************
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
    bookmarks = models.ManyToManyField(
        User, related_name="bookmarked_post", through='Bookmark')
    # ****************************************************************************************
    objects = Manager()

    def __str__(self):
        return(f"Seller: {self.seller} | Title: {self.title} | ID: {self.pk}")

    class Meta:
        verbose_name = 'Post'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Posts'


class MessageThread(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.SET_NULL, null=True, related_name="messageThreads")
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messageThreads')
    archived_by_seller = models.BooleanField(default=False)
    archived_by_buyer = models.BooleanField(default=False)

    date_started = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now=True)

    highlighted_message = models.OneToOneField(
        'Message', on_delete=models.SET_NULL, null=True, blank=True, related_name="highlighted_by")
    pinned_message = models.OneToOneField(
        'Message', on_delete=models.SET_NULL, null=True, blank=True, related_name="pinned_by")

    objects = Manager()

    def __str__(self):
        return(f"Seller: {self.post.seller.username} | Buyer: {self.buyer.username} | ID: {self.pk}")

    class Meta:
        get_latest_by = 'last_updated'
        verbose_name = 'MessageThread'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'MessageThreads'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    messageThread = models.ForeignKey(
        MessageThread, on_delete=models.CASCADE, related_name='messages')

    text = models.CharField(max_length=250)
    image = models.ImageField(blank=True, upload_to='message_pics')
    offer = models.PositiveSmallIntegerField(blank=True, null=True)
    offer_accepted = models.BooleanField(null=True)
    offer_retracted = models.BooleanField(null=True)

    reference = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True)

    time_sent = models.DateTimeField(auto_now_add=True, auto_now=False)
    seen = models.BooleanField(null=True)

    def retractPreviousOffers(self):
        Message.objects.filter(
            sender=self.sender, messageThread=self.messageThread, offer__isnull=False, time_sent__lte=timezone.now()).update(offer_retracted=True)

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        self.messageThread.highlighted_message = self
        self.messageThread.save()

    objects = Manager()

    def __str__(self):
        return(f"Sender: {self.sender.username} | Seen: {self.seen} | ID: {self.pk}")

    class Meta:
        get_latest_by = 'time_sent'
        verbose_name = 'Message'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Messages'


class Bookmark(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date_bookmarked = models.DateTimeField(default=timezone.now)  # UTC time

    objects = Manager()

    def __str__(self):
        return f"Post with id: {self.post.pk} bookmarked by {self.user.username} at time {self.date_bookmarked }"

    class Meta:
        verbose_name = 'Bookmarked Post'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Bookmarked Posts'


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
