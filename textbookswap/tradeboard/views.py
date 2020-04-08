from django.shortcuts import render
from .models import Post
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'tradeboard/home.html', {'posts': posts})


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