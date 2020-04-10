from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tradeboard.models import Post
from PIL import Image


class Profile(models.Model):
    # 1-1 field pointing to correspoding user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

# may need to reconsider the name. For the functionality it is serving right now it maybe batter to just call it bookmarks.


class WishList(models.Model):
    # 1-1 field pointing to correspoding user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return f"{self.user.username}'s wishlist: \n {self.posts.all()}"

    class Meta:
        verbose_name = 'Wishlist'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Wishlists'


# I realize that this isn't part of our MVP but I'm putting it here in case want to implement it
class MessageChain(models.Model):
    # many-1 field pointing to correspoding post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # many-1 field pointing to the seller. Could just reference the 'User' from the 'Post' model but this seemed clearer.
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messagechain_selling")
    # many-1 field pointing to correspoding post
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messagechain_buying")
    # still thinking about how the buyer would reference their message chain

    def __str__(self):
        return f'Massage Chain[Post ID: {post.pk}, Seller: {seller.username}, Buyer: {buyer.username}]'

    class Meta:
        verbose_name = 'Message-Chain'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Message-Chains'


class Message(models.Model):
    chain = models.ForeignKey(
        MessageChain, on_delete=models.CASCADE,  related_name="messages")
    content = models.TextField(max_length=1000)
    time_sent = models.DateTimeField(default=timezone.now)
    # ***************************************************************
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_sent")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_recieved")
    # ***************************************************************
    TEXT = 'Text'
    OFFER = 'Offer'
    message_types = (
        (TEXT, 'Text'),
        (OFFER, 'Offer')
    )
    message_type = models.CharField(max_length=10, choices=message_types)
    # ***************************************************************

    def __str__(self):
        return f'Message [Post: {chain.post.pk}, From: {sender.username}, Buyer: {receiver.username}]'

    class Meta:
        verbose_name = 'Message'
        # Name the model will appear under in the Django Admin page.
        verbose_name_plural = 'Messages'
