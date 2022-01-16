from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='guest_test_user')

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Заголовок тестовой группы',
            slug='test-slug',
            description='Описание тестовой группы',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст тестовой записи',
            group=cls.group,
        )


class PostModelTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_models_have_correct_post_names(self):
        """Проверяем, что у моделей корректно работает __str__, строковое
        представление выводит 15 символов текста поста."""
        self.post = PostModelTest.post
        self.assertEqual(str(self.post), self.post.text[:15])

    def test_models_have_correct_group_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.group = PostModelTest.group
        self.assertEqual(str(self.group), PostModelTest.group.title)
