from .models import Post
import random
import string

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def createInstances(number=10):
    for i in range(number):
        post=Post.objects.create(title=randomString(random.randrange(5,20,1)),ISBN=randomString(13))

def deleteAllInstances():
    Post.objects.all().delete()
