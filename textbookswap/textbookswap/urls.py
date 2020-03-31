from django.contrib import admin
from django.urls import path
from tradeboard import views as tradeboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tradeboard_view.home, name='tradeboard-home')
]
