from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'text': 'Текст записи', 'group': 'Группа'}
        help_texts = {'text': 'Обязательное поле. Добавьте свою запись здесь.',
                      'group': 'Укажите группу для Вашей записи'}
