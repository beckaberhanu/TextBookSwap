from tradeboard.models import Post
from django.utils.lorem_ipsum import WORDS as lorem_words
from django.contrib.auth.models import User
import random
import string


def randomString(stringLength):
    """Generate a random string with the combination of numbers, and lowercase and uppercase letters """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


def randomLorem(stringLength):
    output = ''
    while len(output) < stringLength-20:
        output += ' ' + random.choice(list(lorem_words))
    return output[1].upper()+output[2:]


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
        firstname = randomText(random.randrange(3, 15, 1))
        lastname = randomText(random.randrange(3, 15, 1))
        email = randomString(random.randrange(5, 20, 1))+"@macmail.com"
        while (len(User.objects.filter(username=username)) > 0 or len(User.objects.filter(email=email)) > 0):
            username = randomString(random.randrange(5, 20, 1))
            email = randomString(random.randrange(5, 20, 1))+"@macmail.com"
        password = "Test12345"
        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=firstname, last_name=lastname)


def createPostInstances(number=10):
    for i in range(number):
        user = random.choice(User.objects.all())
        title = randomText(random.randrange(5, 20, 1))
        ISBN = randomNumbers(13)
        author = randomText(random.randrange(5, 20, 1))
        edition = random.randrange(1, 15, 1)
        description = randomLorem(random.randrange(60, 270, 1))
        price = random.randrange(0, 25, 1)
        booktype = random.choice(['Other', 'Textbook'])
        post = Post.objects.create(
            seller=user, title=title, description=description, ISBN=ISBN, author=author, edition=edition, price=price, post_type=booktype)


def createBookmarkInstances(maxnumber=10):
    for user in User.objects.all():
        allPosts = Post.objects.all().exclude(seller=user)
        for i in range(random.randrange(min(maxnumber, len(allPosts)))):
            user.bookmarked_post.add(random.choice(allPosts))


def reinitialize():
    deleteAllPostInstances()
    deleteAllUserInstances()
    # deleteAllWishListInstances()
    createUserInstances()
    createPostInstances()
    # createWishlistInstances()


def deleteAllPostInstances():
    Post.objects.all().delete()


def deleteAllUserInstances():
    User.objects.filter(is_staff=False).delete()


def deleteAllWishListInstances():
    WishList.objects.all().delete()


def createRealInstances():
    titleList = ["Fundamentals of Wavelets",
                 "Data Smart",
                 "God Created the Integers",
                 "Superfreakonomics",
                 "Orientalism",
                 "Nature of Statistical Learning Theory, The Integration of the Indian States",
                 "Drunkard's Walk, The Image Processing & Mathematical Morphology",
                 "How to Think Like Sherlock Holmes",
                 "Data Scientists at Work",
                 "Slaughterhouse Five",
                 "Birth of a Theorem",
                 "Structure & Interpretation of Computer Programs",
                 "Age of Wrath, The Trial, The Statistical Decision Theory"
                 ]
    authorList = [
        "Goswami, Jaideva",
        "Foreman, John",
        "Hawking, Stephen",
        "Dubner, Stephen",
        "Said, Edward",
        "Vapnik, Vladimir",
        "Menon, V P",
        "Mlodinow, Leonard",
        "Shih, Frank",
        "Konnikova, Maria",
        "Sebastian Gutierrez",
        "Vonnegut, Kurt",
        "Villani, Cedric",
    ]

    for i in range(len(titleList)):
        user = random.choice(User.objects.all())
        title = titleList[i]
        ISBN = randomNumbers(13)
        author = authorList[i]
        edition = random.randrange(1, 15, 1)
        description = ("Most existing books on wavelets are either too mathematical or they focus on too narrow a specialty. "
                       "This book provides a thorough treatment of the subject from an engineering point of view. "
                       "It is a one-stop source of theory, algorithms, applications, and computer codes related to wavelets. ")
        price = random.randrange(10, 500, 1)
        booktype = random.choice(['Other', 'Textbook'])
        post = Post.objects.create(
            seller=user, title=title, description=description, ISBN=ISBN, author=author, edition=edition, price=price, post_type=booktype)
