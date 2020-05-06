from django.http import QueryDict
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .forms import BookSearchForm, BookSellForm
from .models import Post
from users.models import Bookmark
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

from django.http import HttpResponse
import json


@login_required
def home(request):
    user = request.user
    posts = Post.objects.exclude(seller=request.user)
    search_form = BookSearchForm()
    if request.method == "POST":
        if request.is_ajax():
            return handleAJAXrequest(request)
        else:
            search_form = BookSearchForm(request.POST)
            if request.POST.get('clear'):
                posts = Post.objects.exclude(seller=request.user)
                search_form = BookSearchForm()
            elif search_form.is_valid():
                posts = search_form.filter()

    bookmarked = []
    if hasattr(user, 'bookmark'):
        bookmarked = user.bookmark.posts.all()

    return render(request, 'tradeboard/home.html', {'search_form': search_form})


def handleAJAXrequest(request):
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
    elif request.POST.get("action") == "loadContact":
        return loadContact(request)
    # popup ****************************************************
    # elif request.POST.get("action") == "edit":
    #     return loadSellList(request)
    elif request.POST.get("action") == "delete":
        return deletePost(request)
    elif request.POST.get("action") == "tag-sold":
        return tagPostSold(request)
    # elif request.POST.get("action") == "contact":
    #     return loadSellList(request)
    elif request.POST.get("action") == "get-new-post-form":
        return getNewPostForm(request)
    else:
        return handleForm(request)


def getNewPostForm(request):
    print('getNewPostForm function called')
    post_form = BookSellForm()
    html = render_to_string('tradeboard/new_post.html',
                            {'post_form': post_form})
    return HttpResponse(html)


def handleForm(request):
    print("wait for it")
    print(request.POST)
    print("request printed")
    if 'description' in request.POST:
        print('check file\n', request.FILES)
        return createNewPost(request)
    else:
        return filterPosts(request)


def createNewPost(request):
    user = request.user
    post_form = BookSellForm(request.POST, request.FILES)
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.seller = user
        post.save()
        return HttpResponse("post was successful")
    else:
        form = render_to_string(
            'tradeboard/new_post.html', {'post_form': post_form})
        return HttpResponse(form, status=400)

# def editPost(request):
#     pass


def deletePost(request):
    id = request.POST.get('post')
    post = Post.objects.get(id=id)
    if request.user == post.seller:
        post.delete()
        return HttpResponse("Post deleted succesfully")
    else:
        raise PermissionDenied
        return HttpResponse("You Don't have access to this post instance", status=400)


def tagPostSold(request):
    id = request.POST.get('post')
    post = Post.objects.get(id=id)
    if request.user == post.seller:
        post.transaction_state = "Complete"
        post.save()
        print("post ", post.title, " sold")
        return HttpResponse("Transaction completed succesfully")
    else:
        return HttpResponse("You Don't have access to this post instance", status=400)


# def contact(request):
#     pass


def loadBookmark(request):
    print("loadBookmark called ")
    if hasattr(request.user, 'bookmark'):
        posts = request.user.bookmark.posts.all()
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'bookmarked': posts, 'tab': 'Bookmark'})
    return HttpResponse(html)


def loadContact(request):
    print("loadContact called ")
    posts = Post.objects.filter(seller=request.user)
    html = render_to_string('tradeboard/contact_detail.html',
                            {'posts': posts.order_by('-date_posted')})
    return HttpResponse(html)


def loadSellList(request):
    print("loadSellList called ")
    bookmarked = []
    if hasattr(request.user, 'bookmark'):
        bookmarked = request.user.bookmark.posts.all()
    posts = Post.objects.filter(
        seller=request.user, transaction_state='In progress')
    posts = posts.order_by('-date_posted')
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'bookmarked': bookmarked, 'tab': 'SellList'})
    return HttpResponse(html)


def clear(request):
    print('clear function called')
    posts = Post.objects.exclude(seller=request.user)
    search_form = BookSearchForm()
    bookmarked = []
    if hasattr(request.user, 'bookmark'):
        bookmarked = request.user.bookmark.posts.all()
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'bookmarked': bookmarked})
    form = render_to_string(
        'tradeboard/searchForm.html', {'search_form': search_form})
    return HttpResponse(json.dumps({'searchResults': html, 'form': form}), content_type="application/json")


def filterPosts(request):
    search_form = BookSearchForm(request.POST)
    if search_form.is_valid():
        posts = search_form.filter().exclude(seller=request.user)
        bookmarked = []
        if hasattr(request.user, 'bookmark'):
            bookmarked = request.user.bookmark.posts.all()
        html = render_to_string('tradeboard/postpopulate.html',
                                {'posts': posts, 'bookmarked': bookmarked})
        form = render_to_string(
            'tradeboard/searchForm.html', {'search_form': search_form})
        return HttpResponse(json.dumps({'searchResults': html, 'form': form}), content_type="application/json")
    else:
        form = render_to_string(
            'tradeboard/searchForm.html', {'search_form': search_form})
        return HttpResponse(form, status=400)


def initialize(request):
    bookmarked = []
    if hasattr(request.user, 'bookmark'):
        bookmarked = request.user.bookmark.posts.all()
    posts = Post.objects.filter(transaction_state='In progress')
    posts = posts.exclude(seller=request.user)
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'bookmarked': bookmarked})
    return HttpResponse(html)


def bookmark(request):
    user = request.user
    pk = request.POST.get("pk")
    post = Post.objects.get(pk=pk)
    bookmarked = False
    if hasattr(user, 'bookmark'):
        if post in user.bookmark.posts.all():
            user.bookmark.posts.remove(post)
            bookmarked = False
        else:
            user.bookmark.posts.add(post)
            bookmarked = True
    else:
        bk = Bookmark(user=user)
        bk.save()
        bk.posts.add(post)
        bookmarked = True
    return HttpResponse(json.dumps({'bookmarked': bookmarked, 'pk': request.POST.get("pk")}), content_type="application/json")


class BookCreateView(CreateView):
    model = Post
    template_name = "tradeboard/new_book.html"
    fields = ['title', 'ISBN', 'author', 'description', 'image',
              'edition', 'price']  # removed the seller field <- becka
    success_url = reverse_lazy('tradeboard-home')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class BookDetailView(DetailView):
    model = Post
    template_name = 'tradeboard/detail_book.html'
    context_object_name = "book"

class BookUpdateView(UpdateView):
    model = Post
    template_name = 'tradeboard/edit_book.html'
    fields = ['title', 'ISBN', 'author',
              'description', 'image', 'edition', 'price']
    success_url = reverse_lazy('tradeboard-home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.seller != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BookDeleteView(DeleteView):
    model = Post
    template_name = 'tradeboard/delete_book.html'
    success_url = reverse_lazy('tradeboard-home')
    context_object_name = "book"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.seller != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class SellingListView(ListView):
    model = Post
    template_name = 'tradeboard/selling_list.html'

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(seller=user)

class ContactDetailView(DetailView):
    model = Post
    template_name = 'tradeboard/contact_detail.html'
    context_object_name = "book"
