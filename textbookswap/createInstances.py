from tradeboard.models import Post
from users.models import WishList
from django.contrib.auth.models import User
import random
import string


def randomString(stringLength):
    """Generate a random string with the combination of numbers, and lowercase and uppercase letters """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


def randomText(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


def randomNumbers(stringLength):
    """Generate a random sequence of numbers of length <stringLength>"""
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


def createUserInstances(number=10):
    for i in range(number):
        username = randomString(random.randrange(5, 20, 1))
        email = randomString(random.randrange(5, 20, 1))+"@macmail.com"
        print("****************************")
        print(len(User.objects.filter(username=username)))
        while (len(User.objects.filter(username=username)) > 0 or len(User.objects.filter(email=email)) > 0):
            username = randomString(random.randrange(5, 20, 1))
            email = randomString(random.randrange(5, 20, 1))+"@macmail.com"
        password = randomString(random.randrange(5, 20, 1))
        user = User.objects.create_user(
            username=username, email=email, password=password)


def createPostInstances(number=10):
    for i in range(number):
        user = random.choice(User.objects.all())
        title = randomText(random.randrange(5, 20, 1))
        ISBN = randomNumbers(13)
        author = randomText(random.randrange(5, 20, 1))
        edition = random.randrange(1, 15, 1)
        description = randomText(random.randrange(200, 900, 1))
        post = Post.objects.create(
            seller=user, title=title, description=description, ISBN=ISBN, author=author, edition=edition)


def createWishlistInstances(maxnumber=10):
    for user in User.objects.all():
        allPosts = Post.objects.all().exclude(seller=user)
        wishList = None
        if(hasattr(user, 'wishlist')):
            wishList = user.wishlist
        else:
            wishList = WishList.objects.create(user=user)
        for i in range(random.randrange(min(maxnumber, len(allPosts)))):
            post = random.choice(allPosts)
            wishList.posts.add(post)


def deleteAllPostInstances():
    Post.objects.all().delete()


def deleteAllUserInstances():
    User.objects.filter(is_staff=False).delete()


def deleteAllWishListInstances():
    WishList.objects.all().delete()
