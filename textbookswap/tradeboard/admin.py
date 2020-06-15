from django.contrib import admin
from .models import Post, Bookmark, MessageThread, Message

admin.site.register(Post)
admin.site.register(Bookmark)
admin.site.register(MessageThread)
admin.site.register(Message)
