from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from .test_models import Post, Group

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='guest_test_user')

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def setUp(self):
        self.post = Post.objects.create(
            author=self.user,  # .get(id=1)
            text='Текст тестовой записи',
            # post_id=PostsURLTests.get(id=1)
        )
        self.group = Group.objects.create(
            title='Заголовок тестовой группы',
            slug='test-slug',
            description='Описание тестовой группы',
        )

    # Проверяем общедоступные страницы
    def test_homepage(self) -> None:
        """Страница / доступна любому пользователю."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_page(self) -> None:
        """Страница group/<slug:slug>/ доступна любому пользователю."""
        response = self.guest_client.get('/group/test-slug/')
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self) -> None:
        """Страница profile/<str:username>/ доступна любому пользователю."""
        response = self.guest_client.get('/profile/guest_test_user/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page(self) -> None:
        """Страница posts/<int:post_id>/ доступна любому пользователю."""
        response = self.guest_client.get('/posts/1/')
        self.assertEqual(response.status_code, 200)

    # Проверяем страницы доступные авторизованным пользователям
    def test_create_page(self) -> None:
        """Страница create/ доступна авторизированному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    # Проверяем страницу редактирования поста, доступную только автору
    def test_edit_post_page(self) -> None:
        """Страница posts/<pk>/edit/ доступна
        авторизированному автору поста."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_create_page_url_redirect_guest_on_login(self) -> None:
        """Страница /create/ перенаправит анонимного пользователя
        на страницу авторизации.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')

    # Проверяем редиректы для неавторизованного пользователя
    # со страницы редактирования поста
    def test_post_detail_page_url_redirect_guest_on_login(self) -> None:
        """Страница /post_detail/ перенаправит анонимного пользователя
        на страницу авторизации.
        """
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/')

    # Проверка вызываемых шаблонов
    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/guest_test_user/',
            'posts/post_detail.html': '/posts/1/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    # Проверка вызываемых шаблонов для страницы новой записи
    def test_create_page_uses_correct_template(self):
        """Страница по адресу / использует шаблон create_post.html."""
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    # Проверка вызываемых шаблонов для страницы редактирования записи
    def test_edit_page_uses_correct_template(self):
        """Страница по адресу / использует шаблон create_post.html."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_wrong_url_returns_404(self):
        response = self.guest_client.get('something/wrong/url/')
        self.assertEqual(response.status_code, 404)
