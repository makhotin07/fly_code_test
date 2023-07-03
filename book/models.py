from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    # Add additional fields for the user profile

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    name = models.CharField(max_length=255, verbose_name='Имя')
    biography = models.TextField(verbose_name='Биография')
    profile_picture = models.ImageField(upload_to='authors', blank=True,
                                        null=True,
                                        verbose_name='Фотография профиля')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name='Автор')
    description = models.TextField(verbose_name='Описание')
    text = models.TextField(verbose_name='Текст')
    archived = models.BooleanField(default=False, verbose_name='Архивировано')
    rating = models.DecimalField(max_digits=5, decimal_places=2,
                                 default=0)
    likes = models.ManyToManyField(User, related_name='liked_books',
                                   blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Книга')
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата и время обновления')

    def __str__(self):
        return f"Комментарий от {self.user.username} к книге '{self.book.title}'"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
