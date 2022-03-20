from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class Test(TestCase):
    user: User
    client: Client
    token: str

    def setUp(self) -> None:
        self.user = User.objects.create_superuser('test', 'test@test.com', '1')
        result = Client().post(reverse('jwt_obtain_token'), data={
            'username': 'test',
            'password': '1',
        })
        self.client = Client(HTTP_AUTHORIZATION="Bearer " + result.json()['access'])

    def test(self):
        self._create()
        self._check_created()
        self._check_redirect()
        self._check_counter()

    def _create(self):
        result = self.client.post(reverse("shorturl-list"), {
            "title": "test",
            "url": "http://google.com"
        })
        self.assertEqual(result.status_code, 201)

    def _check_created(self):
        result = self.client.get(reverse("shorturl-list"))
        self.assertEqual(result.json()['count'], 1)

    def _check_redirect(self):
        result = self.client.get(reverse("shorturl-list"))
        result = Client().get("/r/" + result.json()['results'][0]['slug'] + "/")
        self.assertEqual(result.status_code, 302)

    def _check_counter(self):
        result = self.client.get(reverse("shorturl-list"))
        self.assertEqual(result.json()['results'][0]['counter'], 1)