from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tradeboard.models import Post

# Create your models here.


class Profile(models.Model):
    # 1-1 field pointing to correspoding user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default_profile.png", upload_to="profile_pics")  # saves image to a folder called ../media/profile_pics or references an image located at ../media/default_profile.png if left empty.

    def __str__(self):  # similar to a 'tostring' method in java
        return f"{self.user.username} Profile"


# may need to reconsider the name. For the functionality it is serving right now it maybe batter to just call it bookmarks.
class WishList(models.Model):
    # 1-1 field pointing to correspoding user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.ManyToManyField(Post)

    def __str__(self):
        return f"{self.user.username}'s wishlist: \n {self.posts.all()}"


# I realize that this isn't part of our MVP but I'm putting it here in case want to implement it
# class MessageChain(models.Model):
#     # many-1 field pointing to correspoding post
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     # many-1 field pointing to the seller. Could just reference the 'User' from the 'Post' model but this seemed clearer.
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     # many-1 field pointing to correspoding post
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE)
#     # still thinking about how the buyer would reference their message chain


# class Messages(models.Model):
#     chain = models.ForeignKey(MessageChain, on_delete=models.CASCADE)
#     content = models.TextField(max_length=1000)
#     time_sent = models.DateTimeField(default=timezone)
#     # ***************************************************************
#     SELLER = 'Seller'
#     BUYER = 'Buyer'
#     choices = (
#         (SELLER, 'Seller'),
#         (BUYER, 'Buyer')
#     )
#     sender = models.CharField(max_length=10, choices=choices)
#     # ***************************************************************
#     TEXT = 'Text'
#     OFFER = 'Offer'
#     message_types = (
#         (TEXT, 'Text'),
#         (OFFER, 'Offer')
#     )
#     message_type = models.CharField(max_length=10, choices=message_types)
#     # ***************************************************************
