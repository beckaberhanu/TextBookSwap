from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tradeboard import views as tradeboard_view
from users import views as user_views
from tradeboard.views import BookCreateView, BookDetailView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='edit_book'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='detail_book'),
    path('book/new/', BookCreateView.as_view(), name='book_new'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', tradeboard_view.home, name='tradeboard-home')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
