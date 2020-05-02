from django.http import QueryDict
from django.shortcuts import render
from django.template.loader import render_to_string
from .forms import BookSearchForm
from .models import Post
from users.models import Bookmark
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

    return render(request, 'tradeboard/home.html', {'posts': posts.order_by('-date_posted'), 'bookmarked': bookmarked, 'search_form': search_form})


def handleAJAXrequest(request):
    if request.POST.get("action") == "bookmark":
        return bookmark(request)
    elif request.POST.get("action") == "initialize":
        return initialize(request)
    elif request.POST.get("action") == "switch-tabs":
        pass
    elif request.POST.get("action") == "clear":
        return clear(request)
    else:
        return filterPosts(request)
    # else:
    #     return filterPosts(request)


def clear(request):
    print('clear function called')
    # change this later consider changing intialize too.
    return initialize(request)


def filterPosts(request):
    search_form = BookSearchForm(request.POST)
    if search_form.is_valid():
        posts = search_form.filter()
    bookmarked = []
    if hasattr(request.user, 'bookmark'):
        bookmarked = request.user.bookmark.posts.all()
    posts = search_form.filter()
    html = render_to_string('tradeboard/postpopulate.html',
                            {'posts': posts.order_by('-date_posted'), 'bookmarked': bookmarked})
    return HttpResponse(html)


def initialize(request):
    bookmarked = []
    if hasattr(request.user, 'bookmark'):
        bookmarked = request.user.bookmark.posts.all()
    posts = Post.objects.exclude(seller=request.user)
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


def switchtab(request):
    print("nothing to do here")
    pass


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
