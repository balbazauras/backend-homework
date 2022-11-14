from django.test import TestCase, Client
from service.models import User, Url, Click
from service.utils import STARTING_STRING_ID, get_short_url_base58, get_ip, get_referer
from django.utils import timezone
from django.test.client import RequestFactory


class TestViewS(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_client_login_page(self):
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service/login_user.html')

    def test_short_url_creation(self):

        url = Url.objects.create(
            user=User.objects.create_user(
                username='testuser', password='12345'),
            long_url='https://www.youtube.com/watch?v=hA_VxnxCHbo&ab_channel=TheDumbfounds',
            created_at=timezone.now(),
            expiration_time=timezone.now(),
            active=False,
            click_limit=10,
        )
        url.generate_short_url_base58()

        self.assertEqual(
            url.short_url, get_short_url_base58(1))

    def test_user_register_page(self):
        username = 'testuser'
        user = User.objects.create(username=username)
        user.set_password('12345')
        user.save()
        self.assertEqual(User.objects.filter(username=username).exists(), True)

    def test_user_login(self):
        client = Client()
        username = 'testuser'
        user = User.objects.create(username=username)
        user.set_password('12345')
        user.save()
        logged_in = client.login(username='testuser', password='12345')
        self.assertEqual(logged_in, True)
