
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .test_models import BaseTest, Post

User = get_user_model()


class PostFormTests(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_create_post(self):
        """Валидная форма создает запись post в базе данных."""
        # Подсчитаем количество записей
        posts_count = Post.objects.count()

        # Подготавливаем данные для передачи в форму
        form_data = {
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('posts:create_post'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'guest_test_user'}))
        # Проверяем, создался ли 2й пост, увеличилось ли число постов
        second = Post.objects.get(pk=2)
        self.assertEqual(str(second), form_data['text'])
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Валидная форма изменяет запись поста."""
        # Подготавливаем данные для передачи в форму, редактируем пост
        form_data = {
            'text': 'Изменение поста',
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Проверяем, что запись поста отредактировалась
        self.assertTrue(Post.objects.filter(text=form_data['text']).exists())
        # Проверяем, что количество постов не изменилось
        self.assertEqual(Post.objects.count(), 1)
