from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse

from .models import Author, Book, Comment
from .forms import BookForm, CommentForm


@login_required
def author_list(request):
    """
    Отображает список всех авторов.
    """
    authors = Author.objects.all()
    return render(request, 'author_list.html', {'authors': authors})


@login_required
def book_list(request):
    """
    Отображает список всех книг, которые не являются заархивированными.
    """
    books = Book.objects.filter(archived=False)
    return render(request, 'book_list.html', {'books': books})


@login_required(login_url='login')
def author_book_list(request, author_id):
    """
    Отображает список книг выбранного автора, которые не являются заархивированными.
    """
    author = get_object_or_404(Author, pk=author_id)
    books = author.book_set.filter(archived=False)
    return render(request, 'book_list.html',
                  {'author': author, 'books': books})


@login_required
def add_comment(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            comment = Comment(book=book, content=content)
            comment.save()
            return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
    else:
        form = CommentForm()

    return render(request, 'book_detail.html',
                  {'book': book, 'comment_form': form})


@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    comments = book.comments.all()

    # Handle likes
    if request.method == 'POST':
        if 'like' in request.POST:
            book.likes.add(request.user)
        elif 'unlike' in request.POST:
            book.likes.remove(request.user)
        return redirect('book_detail', book_id=book_id)

    user_liked = book.likes.filter(pk=request.user.pk).exists()

    like_count = book.likes.count()

    context = {
        'book': book,
        'comments': comments,
        'user_liked': user_liked,
        'like_count': like_count,
    }

    return render(request, 'book_detail.html', context)



@login_required
def book_edit(request, book_id):
    """
    Редактирует существующую книгу.
    """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book_id)
    else:
        form = BookForm(instance=book)
    return render(request, 'book_edit.html', {'form': form, 'book': book})


@login_required
def toggle_archived(request, book_id):
    """
    Изменяет флаг Archived у книги на противоположное значение.
    """
    book = get_object_or_404(Book, pk=book_id)
    book.archived = not book.archived
    book.save()
    return redirect('book_list')


@login_required
def delete_book(request, book_id):
    """
    Удаляет книгу.
    """
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('book_list')


@login_required
def delete_comment(request, comment_id):
    """
    Удаляет комментарий.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    book_id = comment.book.id
    comment.delete()
    return redirect('book_detail', book_id=book_id)


@login_required
def edit_comment(request, comment_id):
    """
    Редактирует существующий комментарий.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=comment.book.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment_edit.html',
                  {'form': form, 'comment': comment})


def register(request):
    """
    Регистрация нового пользователя.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('author_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_book_list(request):
    """
    Отображает список книг, добавленных текущим пользователем.
    """
    books = Book.objects.filter(author__user=request.user)
    return render(request, 'user_book_list.html', {'books': books})


def home(request):
    """
    Главная страница сайта.
    """
    return render(request, 'home.html')


@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                author = Author.objects.get(user=request.user)
            except Author.DoesNotExist:
                # Если модель Author не существует для текущего пользователя,
                # создаем новую модель Author и связываем ее с пользователем.
                user = request.user
                author = Author.objects.create(user=user, name=user.username)
            book.author = author
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@login_required
def like_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if user in book.likes.all():
        book.likes.remove(user)
    else:
        book.likes.add(user)

    return HttpResponseRedirect(reverse('book_detail', args=[book_id]))


@login_required
def rate_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user

    if request.method == 'POST':
        rating = request.POST.get('rating')  # Получаем оценку из POST-запроса
        book.rating = rating
        book.save()

    return HttpResponseRedirect(reverse('book_detail', args=[book_id]))
