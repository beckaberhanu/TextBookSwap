from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tradeboard import views as tradeboard_view
from users import views as user_views
from tradeboard.views import BookCreateView, BookDetailView, BookUpdateView, BookDeleteView, SellingListView
from django.views.generic import TemplateView

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/selling/', SellingListView.as_view(), name="selling_books"),
    path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='delete_book'),
    path('book/<int:pk>/edit/', BookUpdateView.as_view(), name='edit_book'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='detail_book'),
    path('contact-info/', TemplateView.as_view(template_name="tradeboard/contact_detail.html"), name='contact_detail'),
    path('book/new/', BookCreateView.as_view(), name='book_new'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', 
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('home/', tradeboard_view.home, name='tradeboard-home')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
