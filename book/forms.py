from django import forms
from .models import Book, Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'text', 'archived']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'text': 'Текст',
            'archived': 'Архивировано',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'text': forms.Textarea(attrs={'rows': 10}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Содержание',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
