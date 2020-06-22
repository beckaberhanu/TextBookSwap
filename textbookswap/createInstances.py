from tradeboard.models import Post, Bookmark, MessageThread, Message
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


def createMessageInstances(maxnumber=10):
    users = User.objects.all()
    # seller
    for user in users:
        if user.posts:
            buyer = random.choice(users.exclude(pk=user.pk))
            thread = MessageThread.objects.create(
                post=random.choice(user.posts.all()), buyer=buyer)
            for i in range(maxnumber):
                Message.objects.create(
                    messageThread=thread, sender=random.choice([user, buyer]), text=randomLorem(random.randrange(30, 170)))


def reinitialize():
    deleteAllPostInstances()
    deleteAllMessageInstances()
    deleteAllUserInstances()
    deleteAllBookmarkInstances()
    createUserInstances()
    createRealPostInstances()
    createBookmarkInstances()


def deleteAllPostInstances():
    Post.objects.all().delete()


def deleteAllUserInstances():
    User.objects.filter(is_staff=False).delete()


def deleteAllMessageInstances():
    MessageThread.objects.all().delete()


def deleteAllBookmarkInstances():
    Bookmark.objects.all().delete()


def createRealPostInstances():
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

    bookList = {
        "To Serve Man": " An ogre cookbook on the delicate art of cooking humans",
        "It's Familiar, But Not Too Familiar": " A guide on how to take care of you're newly acquired companion",
        "Who Moved My Cheese?": " Step by step guide to Mage Hand for beginners",
        "We've All Made Mistakes": " Intro to Necromancy raising your dead wife",
        "Of Fleet and Fancy": " a Novel that tells the tales of Odd Heroes",
        "Are you being invaded?": " A guide book on how to protect one's self from Ogres, Goblins, Kobolds, and woodland critters",
        "Ogre's Guide to tying Knots": " A Simplistic Guide on how to Tie Various Knots",
        "The Fall of Cavour": " A Fictional Piece about the caveman wars",
        "Temina's Guide to Kobolds Volume 1 - 6": " An introductory Field Guide to all the ins and out on Kobolds. (1d6 to see which volume it is)",
        "What Men know about Women": " A Hard cover Book with One Hundred Empty Pages",
        "Friar Albert's Guide to Surviving Traps": " Chalk, rope, torches and a sturdy pole are your best friends. And a brain",
        "Friar Albert's Guide to Forest Trails": " Lichen and moss, you fool. Learn the difference",
        "Friar Albert's Guide to Brewing": " You should probably not be adventuring while doing this",
        "Friar Albert's Guide to the History of [setting]": " Braggins be quiet and pay attention",
        "Friar Albert's Guide to Herbs and Plants": " If you can't remember this then chew on some hemlock for your nerves",
        "Friar Albert's Guide to Publishing Law": " No I can't be held responsible if you only read the byline and then die",
        "Friar Albert's Guide to Fleeing the Academy and Hiding in a Church Cellar": " A Memoir",
        "Beholder in the eye of Beauty": " Classic fashion tips for the beholder in your family",
        "Maps, Maps, Maps": " Tons of maps for your reading pleasure",
        "The Lusty Argonian Maid": " A classic Tamriel tale of a lusty lizardfolk maid",
        "Dr. Harding's Guide to Magic Science": " Dr. Harding's book describes how magic is a hoax to supress scientific explanations of the supernatural",
        "Dungeon Masters and how to find them": " mysterious book describing the seldom-seen beasts",
        "A Monster's Guide to Secret Lairs": " Everything a monster needs to know about making the perfect home",
        "The Faerun Survival Guide [1st edition]": " Written (and illustrated by) St. Moyra of Bron Abbey as the complete reference for would-be adventurers or visiting celestials. Written by a recluse and based on what had been told to the author by word of mouth, it contains many “facts” that should probably not be followed",
        "Behind The Wall": " A book made out human skin. This book is constantly wet and smells like a fresh corpse. This book talks about a seal in a cave underwater. Unsure of why but after reading this you get the feeling that you want to break the seal",
        "Stranger in my dreams": " This book talks about the author recalling a depraved creature who over time got closer and closer to her in her dreams. The book seems to be a diary and was never finished. When you read the last finished page in this book you take 1d8 points of psychic damage",
        "Curiosity Kills the Cat": " When you open this thick maroon colored book you quickly realize there is only one page inside. The text drips onto the floor as soon as you begin to read it. You cannot understand any of the text but you immediately realize the text tells of your demise",
        "Influence of the Ocean": " This book can only be read when near the ocean or on a rainy day. Inside the book talks about a man who is waiting for you in the ocean. He mentions all of the rewards he is keeping for you. If you roll and succeed an insight check DC16 you'll find out that this is man is lying to you. If he is real or not you don't know",
        "Diary of a Thief": " This book is a pocket sized leather diary. Every time a player finishes a page of this book they lose a gold coin Unsure of where it went",
        "Changing Secrets": " This sparkling book smells like incense. Inside the book talks about one of your secrets (ask player). This book when read causes every person in the room to know one secret of yours",
        "Patterns of Behavior": " an anthology of mood effecting quilt work - a small hardcover picture book of patterns that slightly effect one's mood",
        "Timeless Words of Wisdom for the Courtroom, Phrases That Persuade From the Backwoods to the Big City": " This is a full compendium of philosophical and legal summaries that can arm a budding lawyer with a mental skill set to be cunning and out think their opponent",
        "Fifty Shades of Drow": " A bestseller among women, as it details the finer points of the Matriarchal society. With tips on how to properly train and punish your man-servants while maintaining your femininity, this book would be banned if only men would actually read it",
        "Fireside Singalongs": " A simple songbook for bored travelers, with optional sheet music for instrumental accompaniment",
        "Income Management and Financial Assessment": " A book containing several long chapters detailing ways to horde, hide, and invest gold. Hidden within are several nude illustrations of females of the common races",
        "The life and times of Volo": " Autobiographical book featuring the exaggerated and often blatantly false adventures of the well traveled Volo",
        "What To Do When You Find Children": " A guidebook to dealing with found children and other such inconveniences in various dangerous situations",
        "Learn To Read": " An incredibly dense book that details the process of learning the art of reading Common, almost impossible to understand, even for those fluent in Common",
        "Gobbo and Me": " - A children's book about the dangers of befriending Goblins",
        "An Almanack of Practical Mortis": " An exhaustive collection of tables detailing how corpses decompose under various circumstances, along with an appendix that explains step-by-step how to remove maggots, close large wounds, and reset broken bones. If the players obtain it second-hand, bits of paper with names such as 'Aunty Milla' and 'Betrand (4c3r)'' are attached by weak adhesive to some of the pages. A successful Perception check reveals that there are slight remnants of adhesive left above each note, as if someone kept moving the note down the page over time",
        "A Study on Cloud Castles": " This book presents numerous theories on how the giant's fabled cloud castles might work",
        "How to Talk to Gnolls Without Getting Torn to Shreds": " This book is based off of the notes of an ambitious goblin who was evidently torn to shreds",
        "The Beasts of Menita Valley": " A book detailing the magical fauna of a valley you have never heard of",
        "All Horns & Tails? A Beginner's Guide on Everything Tieflings": " Halifar the Bard walks you through the wide and wild world of Tieflings, their heritage, and how to even make friends with our infernal neighbors",
        "1001 Edible & Magical Plants of Chult": " Visiting Chult but not sure what to eat and what to avoid? This information packed book is the definitive guide on navigating the delicious, dangerous gardens of Chult",
        "A Raven Flew Overhead": " The Raven Queen, lady of mystery and intrigue. Misunderstood. Antihero? Quillo Quillorobor delves into the history of this storied individual, parsing fact from fiction. With exclusive interviews with folks who knew her best, all the way from the Shadowfell itself, this book is a must read",
        "Fun With Tears": " A book detailing the magical and alchemical properties of tears",
        "The Social Practices of Various Avian Humanoids": " This book tells you all you need to know about interacting with bird people",
        "Fey'runds Tales": " a children's book of fables",
        "Eye": " A tale of the journey of the company of the eye. Their rise, their fall, their legacy",
        "Naught but the Wind's Caress": " A collection of torrid love stories between a High Elf and their Human lover",
        "Illuminarium Battalia": " A manual of fighting with magic and steel",
        "Where Is The Pancreas, and How To Prepare It": " The cannibal's guide to fine dining",
        "Rock Hard": " The definitive guide to Dwarven diplomacy",
        "Red Goes Faster": " The definitive biography of Zomo the mad goblin who broke out of the celestial sphere and returned to tell about it",
        "Kobold Jokes": " A joke book, written in Draconic. The jokes are terrible, even by Kobold standards",
        "A Treatise On The Non-Existence Of This Treatise": " A small pamphlet that attempts to convince the reader that the pamphlet does not exist, and that it is in fact a figment of the reader's imagination. Despite being written in a very academic and generally formal tone, the arguments within are mostly circular or otherwise fallacious",
        "Dream Journal": " A carefully illustrated dream journal by a famous wizard of old, containing a large amount of arcane truths. The pages have been scrawled with black ink, rendering it illegible",
        "Necromancy for Imbeciles": " An introductory guide to the basics of necromancy. Has been hollowed out to allow for storage, though it appears normal. Contains a skeleton of a large rodent",
        "The Ravings of Garvus[3rd Edition]": " The assorted notes and thoughts of an ancient and powerful wizard from an era long past. His mind was obliterated upon making contact"
    }

    for title in bookList:
        user = random.choice(User.objects.all())
        ISBN = randomNumbers(13)
        author = random.choice(authorList)
        edition = random.randrange(1, 15, 1)
        description = bookList[title]
        price = random.randrange(10, 500, 1)
        booktype = random.choice(['Other', 'Textbook'])
        post = Post.objects.create(
            seller=user, title=title, description=description, ISBN=ISBN, author=author, edition=edition, price=price, post_type=booktype)


bookInteresting = [
    "To Serve Man: An ogre cookbook on the delicate art of cooking humans",
    "It's Familiar, But Not Too Familiar: A guide on how to take care of you're newly acquired companion",
    "Who Moved My Cheese?: Step by step guide to Mage Hand for beginners",
    "We've All Made Mistakes: Intro to Necromancy raising your dead wife",
    "Of Fleet and Fancy: a Novel that tells the tales of Odd Heroes",
    "Are you being invaded?: A guide book on how to protect one's self from Ogres, Goblins, Kobolds, and woodland critters",
    "Ogre's Guide to tying Knots: A Simplistic Guide on how to Tie Various Knots",
    "The Fall of Cavour: A Fictional Piece about the caveman wars",
    "Temina's Guide to Kobolds Volume 1 - 6: An introductory Field Guide to all the ins and out on Kobolds. (1d6 to see which volume it is)",
    "What Men know about Women: A Hard cover Book with One Hundred Empty Pages",
    "Friar Albert's Guide to Surviving Traps: Chalk, rope, torches and a sturdy pole are your best friends. And a brain",
    "Friar Albert's Guide to Forest Trails: Lichen and moss, you fool. Learn the difference",
    "Friar Albert's Guide to Brewing: You should probably not be adventuring while doing this",
    "Friar Albert's Guide to the History of [setting]: Braggins be quiet and pay attention",
    "Friar Albert's Guide to Herbs and Plants: If you can't remember this then chew on some hemlock for your nerves",
    "Friar Albert's Guide to Publishing Law: No I can't be held responsible if you only read the byline and then die",
    "Friar Albert's Guide to Fleeing the Academy and Hiding in a Church Cellar: A Memoir",
    "Beholder in the eye of Beauty: Classic fashion tips for the beholder in your family",
    "Maps, Maps, Maps: Tons of maps for your reading pleasure",
    "The Lusty Argonian Maid: A classic Tamriel tale of a lusty lizardfolk maid",
    "Dr. Harding's Guide to Magic Science: Dr. Harding's book describes how magic is a hoax to supress scientific explanations of the supernatural",
    "Dungeon Masters and how to find them: mysterious book describing the seldom-seen beasts",
    "A Monster's Guide to Secret Lairs: Everything a monster needs to know about making the perfect home",
    "The Faerun Survival Guide [1st edition]: Written (and illustrated by) St. Moyra of Bron Abbey as the complete reference for would-be adventurers or visiting celestials. Written by a recluse and based on what had been told to the author by word of mouth, it contains many “facts” that should probably not be followed",
    "Behind The Wall: A book made out human skin. This book is constantly wet and smells like a fresh corpse. This book talks about a seal in a cave underwater. Unsure of why but after reading this you get the feeling that you want to break the seal",
    "Stranger in my dreams: This book talks about the author recalling a depraved creature who over time got closer and closer to her in her dreams. The book seems to be a diary and was never finished. When you read the last finished page in this book you take 1d8 points of psychic damage",
    "Curiosity Kills the Cat: When you open this thick maroon colored book you quickly realize there is only one page inside. The text drips onto the floor as soon as you begin to read it. You cannot understand any of the text but you immediately realize the text tells of your demise",
    "Influence of the Ocean: This book can only be read when near the ocean or on a rainy day. Inside the book talks about a man who is waiting for you in the ocean. He mentions all of the rewards he is keeping for you. If you roll and succeed an insight check DC16 you'll find out that this is man is lying to you. If he is real or not you don't know",
    "Diary of a Thief: This book is a pocket sized leather diary. Every time a player finishes a page of this book they lose a gold coin Unsure of where it went",
    "Changing Secrets: This sparkling book smells like incense. Inside the book talks about one of your secrets (ask player). This book when read causes every person in the room to know one secret of yours",
    "Patterns of Behavior: an anthology of mood effecting quilt work - a small hardcover picture book of patterns that slightly effect one's mood",
    "Timeless Words of Wisdom for the Courtroom, Phrases That Persuade From the Backwoods to the Big City: This is a full compendium of philosophical and legal summaries that can arm a budding lawyer with a mental skill set to be cunning and out think their opponent",
    "Fifty Shades of Drow: A bestseller among women, as it details the finer points of the Matriarchal society. With tips on how to properly train and punish your man-servants while maintaining your femininity, this book would be banned if only men would actually read it",
    "Where is that dragon egg? A handy tip book for managing clutter in the workshop",
    "Fireside Singalongs: A simple songbook for bored travelers, with optional sheet music for instrumental accompaniment",
    "Income Management and Financial Assessment: A book containing several long chapters detailing ways to horde, hide, and invest gold. Hidden within are several nude illustrations of females of the common races",
    "The life and times of Volo: Autobiographical book featuring the exaggerated and often blatantly false adventures of the well traveled Volo",
    "What To Do When You Find Children: A guidebook to dealing with found children and other such inconveniences in various dangerous situations",
    "Learn To Read: An incredibly dense book that details the process of learning the art of reading Common, almost impossible to understand, even for those fluent in Common",
    "Gobbo and Me: - A children's book about the dangers of befriending Goblins",
    "An Almanack of Practical Mortis: An exhaustive collection of tables detailing how corpses decompose under various circumstances, along with an appendix that explains step-by-step how to remove maggots, close large wounds, and reset broken bones. If the players obtain it second-hand, bits of paper with names such as 'Aunty Milla' and 'Betrand (4c3r)'' are attached by weak adhesive to some of the pages. A successful Perception check reveals that there are slight remnants of adhesive left above each note, as if someone kept moving the note down the page over time",
    "A Study on Cloud Castles: This book presents numerous theories on how the giant's fabled cloud castles might work",
    "How to Talk to Gnolls Without Getting Torn to Shreds: This book is based off of the notes of an ambitious goblin who was evidently torn to shreds",
    "The Beasts of Menita Valley: A book detailing the magical fauna of a valley you have never heard of",
    "All Horns & Tails? A Beginner's Guide on Everything Tieflings: Halifar the Bard walks you through the wide and wild world of Tieflings, their heritage, and how to even make friends with our infernal neighbors",
    "1001 Edible & Magical Plants of Chult: Visiting Chult but not sure what to eat and what to avoid? This information packed book is the definitive guide on navigating the delicious, dangerous gardens of Chult",
    "A Raven Flew Overhead: The Raven Queen, lady of mystery and intrigue. Misunderstood. Antihero? Quillo Quillorobor delves into the history of this storied individual, parsing fact from fiction. With exclusive interviews with folks who knew her best, all the way from the Shadowfell itself, this book is a must read",
    "Fun With Tears: A book detailing the magical and alchemical properties of tears",
    "The Social Practices of Various Avian Humanoids: This book tells you all you need to know about interacting with bird people",
    "Fey'runds Tales: a children's book of fables",
    "Eye: A tale of the journey of the company of the eye. Their rise, their fall, their legacy",
    "Naught but the Wind's Caress: A collection of torrid love stories between a High Elf and their Human lover",
    "Illuminarium Battalia: A manual of fighting with magic and steel",
    "Where Is The Pancreas, and How To Prepare It: The cannibal's guide to fine dining",
    "Rock Hard: The definitive guide to Dwarven diplomacy",
    "Red Goes Faster: The definitive biography of Zomo the mad goblin who broke out of the celestial sphere and returned to tell about it",
    "The Skull - A heavy book filled with a long stream-of-consciousness narrative describing a single humanoid skull in careful detail. The narrator seems completely focused on the skull, never describing its origins, its surroundings, or themselves",
    "Kobold Jokes: A joke book, written in Draconic. The jokes are terrible, even by Kobold standards",
    "A Treatise On The Non-Existence Of This Treatise: A small pamphlet that attempts to convince the reader that the pamphlet does not exist, and that it is in fact a figment of the reader's imagination. Despite being written in a very academic and generally formal tone, the arguments within are mostly circular or otherwise fallacious",
    "Dream Journal: A carefully illustrated dream journal by a famous wizard of old, containing a large amount of arcane truths. The pages have been scrawled with black ink, rendering it illegible",
    "Necromancy for Imbeciles: An introductory guide to the basics of necromancy. Has been hollowed out to allow for storage, though it appears normal. Contains a skeleton of a large rodent",
    "The Ravings of Garvus[3rd Edition]: The assorted notes and thoughts of an ancient and powerful wizard from an era long past. His mind was obliterated upon making contact"
]
