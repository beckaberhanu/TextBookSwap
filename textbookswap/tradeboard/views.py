from django.shortcuts import render
from .forms import BookSearchForm
from .models import Post
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


@login_required
def home(request):
    posts = Post.objects.all()
    search_form = BookSearchForm()
    if request.method == "POST":
        search_form = BookSearchForm(request.POST)
        if request.POST.get('clear'):
            posts = Post.objects.all()
            search_form = BookSearchForm()
        elif search_form.is_valid():
            posts = search_form.filter()
    return render(request, 'tradeboard/home.html', {'posts': posts, 'search_form': search_form})


class BookCreateView(CreateView):
    model = Post
    template_name = "tradeboard/new_book.html"
    fields = ['seller', 'title', 'ISBN', 'author', 'description', 'image',
              'edition', 'price']  # remember to take out seller later Nadav!
    success_url = reverse_lazy('tradeboard-home')


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
