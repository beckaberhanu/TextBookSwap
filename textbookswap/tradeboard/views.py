from django.shortcuts import render
from .models import Post
from .instances import createInstances
from .instances import deleteAllInstances
from django.views.generic.edit import CreateView

# Create your views here.
def home(request):
    createInstances()
    return render(request, 'tradeboard/home.html')

class BookCreateView(CreateView):
    model = Post
    template_name = "tradeboard/new_book.html"
    fields = '__all__'