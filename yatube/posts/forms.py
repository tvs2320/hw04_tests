from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # # Код для спринта 6, отключено для прохождения тестов спринта 5
        # fields = ('text', 'group', 'image')
        # labels = {'text': 'Текст записи', 'group': 'Группа',
        #           'image': 'Картинка'}
        # help_texts = {'text': 'Обязательное поле. '
        #                       'Добавьте свою запись здесь.',
        #               'group': 'Укажите группу для Вашей записи',
        #               'image': 'Загрузите изображение для Вашей записи'}
        fields = ('text', 'group')
        labels = {'text': 'Текст записи', 'group': 'Группа'}
        help_texts = {'text': 'Обязательное поле. '
                              'Добавьте свою запись здесь.',
                      'group': 'Укажите группу для Вашей записи'
                      }
