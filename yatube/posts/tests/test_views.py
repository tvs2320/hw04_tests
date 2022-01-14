from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .test_models import Post, Group


User = get_user_model()


class PostsViewsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='guest_test_user')

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def setUp(self) -> None:
        self.group = Group.objects.create(
            title='Заголовок тестовой группы',
            slug='test-slug',
            description='Описание тестовой группы',
        )

        number_of_posts = 13
        for self.post in range(number_of_posts):
            Post.objects.create(
                author=self.user,  # (id=1)
                text='Текст тестовой записи',
                group=self.group,
            )

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'}),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'guest_test_user'}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': 1}),
            'posts/create_post.html': reverse(
                'posts:create_post'),
        }

        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

        # Проверяем, что при обращении к name для страницы редактирования поста
        # вызывается соответствующий HTML-шаблон

    def test_edit_page_authorized_uses_correct_template(self) -> None:
        """URL-адрес использует шаблон posts/create_post.html."""
        response = self.authorized_client.get(reverse('posts:post_edit',
                                                      kwargs={'post_id': 1}))
        self.assertTemplateUsed(response, 'posts/create_post.html')

        # Проверяем словарь context в шаблоне главной страницы

    def test_index_page_show_correct_context(self) -> None:
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTrue('paginator' in response.context)
        self.assertTrue('page_number' in response.context)
        self.assertTrue('page_obj' in response.context)

    # Проверяем работу paginator для главной страницы, на первой странице
    # должно быть 10 постов
    def test_first_index_page_contains_ten_posts(self) -> None:
        """Проверяем работу paginator для главной страницы,
        на первой странице должно быть 10 постов"""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

        # Проверка: на второй странице должно быть три поста.
    def test_second_index_page_contains_three_posts(self):
        """Проверяем работу paginator для главной страницы, на второй
        странице должно быть 10 постов"""
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    # Проверяем словарь context в шаблоне страницы групп
    def test_group_list_page_show_correct_context(self) -> None:
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        self.assertTrue('paginator' in response.context)
        self.assertTrue('page_number' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('group' in response.context)

    # Проверяем работу paginator для страницы групп
    # Проверка: количество постов на первой странице групп равно 10.
    def test_first_group_list_page_contains_ten_posts(self) -> None:
        """Проверяем работу paginator для страницы групп, на первой странице
        должно быть 10 постов"""
        response = self.client.get(reverse('posts:group_list',
                                           kwargs={'slug': 'test-slug'}))
        self.assertEqual(len(response.context['page_obj']), 10)

        # Проверка: на второй странице групп должно быть три поста.
    def test_second_group_list_page_contains_three_posts(self):
        """Проверяем работу paginator для страницы групп, на второй странице
        должно быть 3 поста"""
        response = self.client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    # Проверяем словарь context в шаблоне страницы профиля пользователя
    def test_profile_page_show_correct_context(self) -> None:
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:profile', kwargs={'username': 'guest_test_user'}))
        self.assertTrue('author' in response.context)
        self.assertTrue('paginator' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('posts_count' in response.context)
        self.assertTrue('username' in response.context)

    # Проверяем работу paginator для страницы профиля, на первой странице
    # должно быть 10 постов
    def test_first_profile_page_contains_ten_posts(self) -> None:
        """Проверяем работу paginator для страницы profile,
        на первой странице должно быть 10 постов"""
        response = self.client.get(
            reverse('posts:profile', kwargs={'username': 'guest_test_user'}))
        self.assertEqual(len(response.context['page_obj']), 10)

        # Проверка: на второй странице должно быть три поста.
    def test_second_profile_page_contains_three_posts(self):
        """Проверяем работу paginator для страницы profile, на второй
        странице должно быть 3 поста"""
        response = self.client.get(
            reverse('posts:profile', kwargs={
                'username': 'guest_test_user'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    # Проверка словаря контекста страницы создания поста
    def test_create_post_page_show_correct_context(self):
        """Шаблон create_post для страницы создания поста
        сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:create_post'))
        self.assertTrue('form' in response.context)

    # Проверка словаря контекста страницы редактирования поста
    def test_edit_post_page_show_correct_context(self):
        """Шаблон create_post для страницы редактирования
        поста сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:create_post'))
        self.assertTrue('form' in response.context)
        self.assertTrue('user' in response.context)

    # Проверка доступности поста с группой
    def test_post_with_group(self):
        """Пост с группой доступен на главной странице, на странице групп
         и на странице пользователя создавшего пост"""
        Post.objects.create(
            author=self.user,
            text='Текст тестовой записи 14',
            group=self.group,
        )
        Group.objects.create(
            title='Заголовок тестовой группы N2',
            slug='second_test-slug',
            description='Описание тестовой группы N2',
        )
        print(f'Всего создано {Post.objects.count()} постов')

        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

        response = self.client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

        response = self.client.get(
            reverse('posts:profile', kwargs={
                'username': 'guest_test_user'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

        response = self.client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'second_test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj'],), 0)
