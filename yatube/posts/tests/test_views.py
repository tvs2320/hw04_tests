from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

# from tests.fixtures.fixture_data import group
# from tests.fixtures.fixture_user import user

from .test_models import BaseTest, Group, Post

User = get_user_model()


class PostsViewsTests(BaseTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем к тестовому посту еще 12 дополнительно"
        number_of_posts = 12
        for post in range(number_of_posts):
            Post.objects.create(
                author=cls.user,
                text='Текст тестовой записи',
                group=cls.group,
            )

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self) -> None:
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': 'guest_test_user'}
                    ): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': 1}): 'posts/post_detail.html',
            reverse('posts:create_post'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': 1}): 'posts/create_post.html',
        }

        # Проверяем, что при обращении к name вызывается
        # соответствующий HTML-шаблон
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверяем pagination
    def test_pagination(self) -> None:
        """Проверяем работу paginator для главной страницы,
        страницы групп и страницы автора - на первой странице 10 постов,
        на второй странице - 3 поста"""
        # Собираем в словарь пары "reverse(name):
        # количество постов на странице"
        print(f'постов для проверки паджинации: {Post.objects.count()}')
        dict_pages_page_limit = {
            reverse('posts:index'): settings.PAGE_LIMIT,
            reverse('posts:index') + '?page=2': 3,
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}): settings.PAGE_LIMIT,
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}) + '?page=2': 3,
            reverse('posts:profile', kwargs={
                'username': 'guest_test_user'}): settings.PAGE_LIMIT,
            reverse('posts:profile', kwargs={
                'username': 'guest_test_user'}) + '?page=2': 3,
        }
        for reverse_name, page_limit in dict_pages_page_limit.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.client.get(reverse_name)
                self.assertEqual(len(response.context['page_obj']), page_limit)

        # Проверяем словарь context в шаблоне главной страницы
    def test_index_page_show_correct_context(self) -> None:
        """Шаблон index сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('posts:index'))
        self.assertTrue('paginator' in response.context)
        self.assertTrue('page_number' in response.context)
        self.assertTrue('page_obj' in response.context)

    # Проверяем словарь context в шаблоне страницы групп
    def test_group_list_page_show_correct_context(self) -> None:
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        self.assertTrue('paginator' in response.context)
        self.assertTrue('page_number' in response.context)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue('group' in response.context)

    # Проверяем словарь context в шаблоне страницы профиля пользователя
    def test_post_detail_correct_context(self) -> None:
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': 11}))
        self.assertTrue('post_card' in response.context)
        self.assertTrue('posts_count' in response.context)

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
        """Новый пост с указанной группой доступен на главной странице,
        на странице группы, и на странице автора"""
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

        # Собираем в пары reverse_name и количество постов на странице, к
        # предыдущим 13 постам должен добавиться еще один, 14-й
        dict_pages_page_count = {
            reverse('posts:index') + '?page=2': 4,
            reverse('posts:group_list',
                    kwargs={'slug': 'test-slug'}) + '?page=2': 4,
            reverse('posts:profile', kwargs={
                'username': 'guest_test_user'}) + '?page=2': 4,
        }
        for pages, page_count in dict_pages_page_count.items():
            with self.subTest(pages=pages):
                response = self.client.get(pages)
                self.assertEqual(len(response.context['page_obj']), page_count)

        # Проверка, что пост не попал во вторую группу
        response = self.client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'second_test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj'], ), 0)
