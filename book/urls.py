from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Публичная часть сайта
    path('', views.home, name='home'),
    path('authors/', views.author_list, name='author_list'),
    path('books/', views.book_list, name='book_list'),
    path('authors/<int:author_id>/', views.author_book_list,
         name='author_book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),

    # Функции администратора
    path('books/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:book_id>/toggle_archived/', views.toggle_archived,
         name='toggle_archived'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('comments/<int:comment_id>/delete/', views.delete_comment,
         name='delete_comment'),
    path('comments/<int:comment_id>/edit/', views.edit_comment,
         name='edit_comment'),
    path('user_books/', views.user_book_list, name='user_book_list'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'),
         name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/add_comment/', views.add_comment,
         name='add_comment'),
    path('book/<int:book_id>/rate/', views.rate_book, name='rate_book'),
    path('book/<int:book_id>/like/', views.like_book, name='like_book'),

]
