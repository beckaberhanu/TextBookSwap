from django.shortcuts import render
from .models import Post
from .instances import createInstances
from .instances import deleteAllInstances

# Create your views here.
def home(request):
    createInstances()
    return render(request, 'tradeboard/home.html')
