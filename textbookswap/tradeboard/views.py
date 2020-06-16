from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import BookSearchForm, BookSellForm, MessagingForm
from .models import Post, Bookmark, MessageThread, Message
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import BooleanField, Case, Value, When
from django.db import models
import json


@login_required
def home(request):
    """function based view for homepage"""
    user = request.user
    posts = Post.objects.exclude(seller=request.user)
    search_form = BookSearchForm()
    if request.method == "POST":
        if request.is_ajax():
            return handleAJAXrequest(request)

    bookmarked = []
    if hasattr(user, 'bookmark'):
        bookmarked = user.bookmark.posts.all()

    return render(request, 'tradeboard/home.html', {'search_form': search_form})


def handleAJAXrequest(request):
    """sends ajax requests to the proper function"""
    if request.POST.get("action") == "bookmark":
        return bookmark(request)
    elif request.POST.get("action") == "initialize":
        return initialize(request)
    elif request.POST.get("action") == "clear":
        return clear(request)
    elif request.POST.get("action") == "loadTradeboard":
        return initialize(request)
    elif request.POST.get("action") == "loadBookmarks":
        return loadBookmark(request)
    elif request.POST.get("action") == "loadSellList":
        return loadSellList(request)
    elif request.POST.get("action") == "delete":
        return deletePost(request)
    elif request.POST.get("action") == "tag-sold":
        return tagPostSold(request)
    elif request.POST.get("action") == "get-new-post-form":
        return getNewPostForm(request)
    elif request.POST.get("action") == "get-edit-post-form":
        return getEditPostForm(request)
    elif request.POST.get("action") == "load-buyers-tab":
        return loadBuyersTab(request)
    elif request.POST.get("action") == "load-sellers-tab":
        return loadSellersTab(request)
    elif request.POST.get("action") == "load-message-thread":
        return loadMessageThread(request)
    elif request.POST.get("action") == "send-message":
        return sendMessage(request)
    else:
        return handleForm(request)


def sendMessage(request):
    user = request.user
    messageThread = MessageThread.objects.get(
        pk=request.POST.get("messageThread"))
    if(messageThread.buyer == user or messageThread.post.seller == user):
        message_form_recieved = MessagingForm(request.POST, request.FILES)
        if message_form_recieved.is_valid():
            message = message_form_recieved.save(commit=False)
            message.sender = user
            message.messageThread = messageThread
            message.save()
            message_form = MessagingForm()
            html = render_to_string('tradeboard/components/message_chat_screen.html',
                                    {'context': messageThread, 'message_form': message_form}, request)
            return HttpResponse(html)


def loadBuyersTab(request):
    user = request.user
    posts = user.posts.annotate(messageThreads_count=models.Count(
        'messageThreads')).filter(messageThreads_count__gt=0)
    html = render_to_string('tradeboard/components/message_tab_buyers.html',
                            {'context': posts}, request)
    return HttpResponse(html)


def loadSellersTab(request):
    user = request.user
    messageThreads = user.messageThreads.all()
    html = render_to_string('tradeboard/components/message_tab_sellers.html',
                            {'context': messageThreads}, request)
    return HttpResponse(html)


def loadMessageThread(request):
    user = request.user
    messageThread = MessageThread.objects.get(pk=request.POST.get("id"))
    if(messageThread.buyer == user or messageThread.post.seller == user):
        message_form = MessagingForm()
        html = render_to_string('tradeboard/components/message_chat_screen.html',
                                {'context': messageThread, 'message_form': message_form}, request)
        return HttpResponse(html)
    else:
        HttpResponse(status=403)


def getNewPostForm(request):
    """renders and returns an html form for creating new posts"""
    print('getNewPostForm function called')
    post_form = BookSellForm()
    html = render_to_string('tradeboard/new_post.html',
                            {'post_form': post_form, 'action': 'new-post'}, request)
    return HttpResponse(html)


def getEditPostForm(request):
    """renders and returns an editing form for editing existing posts"""
    post = Post.objects.get(pk=request.POST['post'])
    post_form = BookSellForm(instance=post)
    html = render_to_string('tradeboard/new_post.html',
                            {'post_form': post_form, 'action': 'edit', 'post': post}, request)
    return HttpResponse(html)


def handleForm(request):
    """sends information from incoming forms to the proper function to respond to them"""
    if 'description' in request.POST:
        if request.POST['action'] == 'edit':
            return editPost(request)
        elif request.POST.get('action') == 'new-post':
            return createNewPost(request)
    else:
        return filterPosts(request)


def createNewPost(request):
    """accepts information from an incoming post creation form and either updates the database or returns an error"""
    user = request.user
    post_form = BookSellForm(request.POST, request.FILES)
    validity = post_form.is_valid()
    print("is the form valid?", validity)
    if validity:
        post = post_form.save(commit=False)
        post.seller = user
        post.save()
        return HttpResponse("post was successful")
    else:
        form = render_to_string(
            'tradeboard/new_post.html', {'post_form': post_form, 'action': 'new-post'}, request)
        return HttpResponse(form, status=400)


def editPost(request):
    """accepts information from an incoming post editing form and either updates the database or returns an error"""
    id = request.POST['post']
    user = request.user
    post = Post.objects.get(id=id)
    if user == post.seller:
        post_form = BookSellForm(request.POST, request.FILES, instance=post)
        valid = post_form.is_valid()
        if valid:
            post_form.save()
            return HttpResponse("post was successful")
        else:
            form = render_to_string(
                'tradeboard/new_post.html', {'post_form': post_form}, request)
            return HttpResponse(form, status=400)


def deletePost(request):
    """accepts a request with the id of a post and either deletes it or returns an error"""
    id = request.POST.get('post')
    post = Post.objects.get(id=id)
    if request.user == post.seller:
        post.delete()
        return HttpResponse("Post deleted succesfully")
    else:
        raise PermissionDenied
        return HttpResponse("You Don't have access to this post instance", status=400)


def tagPostSold(request):
    """accepts a request with the id of a post and either tags it as 'complete' in the database or returns an error"""
    id = request.POST.get('post')
    post = Post.objects.get(id=id)
    if request.user == post.seller:
        post.transaction_state = "Complete"
        post.save()
        return HttpResponse("Transaction completed succesfully")
    else:
        raise PermissionDenied
        return HttpResponse("You Don't have access to this post instance", status=400)


def loadBookmark(request):
    """renders and returns an html with all bookmarked posts"""
    user = request.user
    bookmarks = user.bookmarked_post.all().annotate(
        bookmarked=Case(default=Value(True), output_field=BooleanField(),))
    if_empty = {
        'small': 'Posts that you have bookmarked will show up in this tab',
        'main': "It seems that you don't have anything bookmarked at the moment."
    }
    print("bookmarks: ====> ", bookmarks)
    bookmarks = bookmarks.order_by('-bookmark__date_bookmarked')
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': bookmarks, 'tab': 'Bookmark', 'if_empty': if_empty}, request)
    return HttpResponse(html)


def loadSellList(request):
    """renders and returns an html with all posts being sold by the current user"""
    posts = Post.objects.filter(
        seller=request.user, transaction_state='In progress').annotate(bookmarked=Case(When(bookmarks__in=[request.user], then=Value(True)), default=Value(False), output_field=BooleanField(),))
    posts = posts.order_by('-date_posted')
    if_empty = {
        'main': "Hi there! It looks like you haven't put up anything for sale yet.",
        'small': 'Click on \'Sell A Book\' above and fill out the form to to put up a book for sell'
    }
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'tab': 'SellList', 'if_empty': if_empty}, request)
    return HttpResponse(html)


def clear(request):
    """clears search filters and returns a new empty search form"""
    search_form = BookSearchForm()
    form = render_to_string(
        'tradeboard/searchForm.html', {'search_form': search_form}, request)
    return HttpResponse(form)


def filterPosts(request):
    """accepts a search form through the request and returns posts that match the data from the search form"""
    search_form = BookSearchForm(request.POST)
    if search_form.is_valid():
        posts = search_form.filter().exclude(seller=request.user).annotate(bookmarked=Case(When(
            bookmarks__in=[request.user], then=Value(True)), default=Value(False), output_field=BooleanField(),))
        bookmarked = []
        if hasattr(request.user, 'bookmark'):
            bookmarked = request.user.bookmark.posts.all()
        if_empty = {
            'main': "Sorry! It seems we don't have anybooks that match your search",
            'small': 'Try slightly tweaking or removing some filters to see that works better'
        }
        html = render_to_string('tradeboard/postpopulate.html',
                                {'posts': posts, 'bookmarked': bookmarked, 'tab': 'Tradeboard', 'if_empty': if_empty}, request)
        form = render_to_string(
            'tradeboard/searchForm.html', {'search_form': search_form}, request)
        return HttpResponse(json.dumps({'searchResults': html, 'form': form}), content_type="application/json")
    else:
        form = render_to_string(
            'tradeboard/searchForm.html', {'search_form': search_form}, request)
        return HttpResponse(form, status=400)


def initialize(request):
    """returns the tradeboard in it's default state"""
    posts = Post.objects.filter(transaction_state='In progress').annotate(bookmarked=Case(When(
        bookmarks__in=[request.user], then=Value(True)), default=Value(False), output_field=BooleanField(),))
    posts = posts.exclude(seller=request.user)
    if_empty = {
        'main': "Sorry! It seems that there are no books being sold here at the moment.",
        'small': 'Come back a different time and maybe you\'ll have better luck'
    }
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'tab': 'Tradeboard', 'if_empty': if_empty}, request)
    return HttpResponse(html)


def bookmark(request):
    """accepts the id of a post through the request and and bookmark it"""
    user = request.user
    pk = request.POST.get("pk")
    post = Post.objects.get(pk=pk)
    if post.bookmarks.filter(bookmark__user=user).exists():
        post.bookmarks.remove(user)
        bookmarked = False
    else:
        post.bookmarks.add(user)
        bookmarked = True
    return HttpResponse(json.dumps({'bookmarked': bookmarked, 'pk': pk}), content_type="application/json")


class ContactDetailView(DetailView):
    """Class based view for displaying contact information for a particular post"""
    model = Post
    template_name = 'tradeboard/contact_detail.html'
    context_object_name = "book"
