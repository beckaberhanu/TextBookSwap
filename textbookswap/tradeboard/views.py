from django.shortcuts import render
from .models import Post
from .instances import createInstances, deleteAllInstances
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    createInstances()
    return render(request, 'tradeboard/home.html')

class BookCreateView(CreateView):
    model = Post
    template_name = "tradeboard/new_book.html"
    fields = '__all__'
    success_url = reverse_lazy('tradeboard-home')