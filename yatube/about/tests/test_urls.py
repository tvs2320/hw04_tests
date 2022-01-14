
from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self) -> None:
        self.guest_client = Client()

    def test_author_page(self) -> None:
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_tech_page(self) -> None:
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_author_page_uses_correct_template(self):
        """Проверка шаблона для адреса /about/author/"""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/author.html')

    def test_tech_page_uses_correct_template(self):
        """Проверка шаблона для адреса /about/author/"""
        response = self.guest_client.get('/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')
