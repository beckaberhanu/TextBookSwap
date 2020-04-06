from django.shortcuts import render
from .models import Post
from django.views.generic.edit import CreateView
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
