from django.shortcuts import render
from .forms import BookSearchForm
from .models import Post
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.


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
            if search_filters['title']:
                posts = posts.filter(title=search_filters['title'])
            if search_filters['author']:
                posts = posts.filter(author=search_filters['author'])
            if search_filters['edition']:
                posts = posts.filter(edition=search_filters['edition'])
            if search_filters['price']:
                posts = posts.filter(price__lte=search_filters['price'])
            if search_filters['posted_since']:
                posts = posts.filter(
                    date_posted__gte=search_filters['posted_since'])
            if search_filters['ISBN']:
                posts = posts | Post.objects.filter(
                    ISBN=search_filters['ISBN'])
    return render(request, 'tradeboard/home.html', {'posts': posts, 'search_form': search_form})


class BookCreateView(CreateView):
    model = Post
    template_name = "tradeboard/new_book.html"
    fields = '__all__'
    success_url = reverse_lazy('tradeboard-home')


class BookDetailView(DetailView):
    model = Post
    template_name = 'tradeboard/detail_book.html'
    context_object_name = "book"


class BookUpdateView(UpdateView):
    model = Post
    template_name = 'tradeboard/edit_book.html'
    fields = '__all__'


class BookDeleteView(DeleteView):
    model = Post
    template_name = 'tradeboard/delete_book.html'
    success_url = reverse_lazy('tradeboard-home')
    context_object_name = "book"
