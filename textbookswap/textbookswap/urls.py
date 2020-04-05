from django.contrib import admin
from django.urls import path
from tradeboard import views as tradeboard_view
from users import views as user_views
from tradeboard.views import BookCreateView

urlpatterns = [
    path('book/new/', BookCreateView.as_view(), name='book_new'),
    path('admin/', admin.site.urls),
    path('register/',user_views.register, name='register'),
    path('', tradeboard_view.home, name='tradeboard-home')
]
