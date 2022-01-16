from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тест' * 5,
        )

    def test_models_have_correct_post_names(self):
        """Проверяем, что у моделей корректно работает __str__, строковое
        представление выводит 15 символов текста поста."""
        post = PostModelTest.post
        self.assertEqual(str(post), post.text[:15])

    def test_models_have_correct_group_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        self.assertEqual(str(group), group.title)
