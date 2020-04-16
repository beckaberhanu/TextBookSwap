from django.shortcuts import render
from .forms import BookSearchForm
from .models import Post
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
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
            search_filters = search_form.cleaned_data
            posts = Post.objects.all()
            print(posts)
            if search_filters['title']:
                print('title')
                posts = posts.filter(title=search_filters['title'])
            if search_filters['author']:
                print('author')
                posts = posts.filter(author=search_filters['author'])
            if search_filters['edition']:
                print('edition')
                posts = posts.filter(edition=search_filters['edition'])
            if search_filters['ISBN']:
                print('isbn')
                posts = posts | Post.objects.filter(
                    ISBN=search_filters['ISBN'])
                print(posts)
            if search_filters['price']:
                print('price')
                posts = posts.filter(price__lte=search_filters['price'])
            if search_filters['posted_since']:
                print('postedsince')
                posts = posts.filter(
                    date_posted__gte=search_filters['posted_since'])
                print(posts)
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

    # https://stackoverflow.com/questions/48143089/django-display-data-for-current-user-only
    # def get_queryset(self):
    #     user = self.request.user
    #     adaccount_list = Account.objects.filter(user=user)\
    #                      .values_list('adaccounts', flat=True)
    #     return Performance.objects.filter(adaccount__in=adaccount_list)
