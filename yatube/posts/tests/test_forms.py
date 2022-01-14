from .test_models import Post, Group
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='guest_test_user')

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.form = PostForm()

    def setUp(self):
        self.group = Group.objects.create(
            title='Заголовок тестовой группы',
            slug='test-slug',
            description='Описание тестовой группы',
        )

        self.post = Post.objects.create(
            author=self.user,  # .get(id=1)
            text='Текст тестовой записи',
            group=self.group,
        )

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
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Валидная форма изменяет запись поста."""
        # Создадим запись 2
        second_post = Post.objects.create(
            author=self.user,
            text='Текст тестовой записи2',
            group=self.group,
        )

        # Подготавливаем данные для передачи в форму, редактируем пост
        form_data = {
            'text': 'Изменение текста записи',
            'group': self.group,
        }
        # Проверяем, что текст поста изменился
        self.assertNotEqual(Post.text, form_data['text'])
        # Проверяем, что количество постов не изменилось
        self.assertEqual(Post.objects.count(), 2)
        # Проверяем, что вызывается страница детализации поста
        response = self.authorized_client.post(
            reverse('posts:post_detail', kwargs={'post_id': 1}),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
