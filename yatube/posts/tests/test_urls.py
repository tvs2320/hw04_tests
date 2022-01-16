from http import HTTPStatus

from django.contrib.auth import get_user_model

from .test_models import BaseTest

User = get_user_model()


class PostsURLTests(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
    #
    #     cls.guest_client = Client()
    #     cls.user = User.objects.create_user(username='guest_test_user')
    #
    #     cls.authorized_client = Client()
    #     cls.authorized_client.force_login(cls.user)
    #
    # def setUp(self):
    #     self.post = Post.objects.create(
    #         author=self.user,
    #         text='Текст тестовой записи',
    #     )
    #     self.group = Group.objects.create(
    #         title='Заголовок тестовой группы',
    #         slug='test-slug',
    #         description='Описание тестовой группы',
    #     )

    # Проверяем страницы доступные неавторизованному пользователю
    def test_homepage(self) -> None:
        """Проверяем страницы доступные неавторизованному пользователю"""
        dict_url_status = {
            '/': HTTPStatus.OK,
            '/group/test-slug/': HTTPStatus.OK,
            '/profile/guest_test_user/': HTTPStatus.OK,
            '/posts/1/': HTTPStatus.OK
        }
        for url, status in dict_url_status.items():
            with self.subTest(status=HTTPStatus):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status)

    # Проверяем страницы доступные авторизованным пользователям
    def test_create_page(self) -> None:
        """Страница create/ доступна авторизированному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Проверяем страницу редактирования поста, доступную только автору
    def test_edit_post_page(self) -> None:
        """Страница posts/<pk>/edit/ доступна
        авторизированному автору поста."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

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
        dict_url_template = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/profile/guest_test_user/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            '/posts/1/edit/': 'posts/create_post.html',
        }
        for url, template in dict_url_template.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_wrong_url_returns_404(self):
        response = self.guest_client.get('something/wrong/url/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
