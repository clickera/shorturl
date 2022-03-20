from base64 import urlsafe_b64encode
from os import urandom

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager


def _get_new_slug(slug=None):
        def _get_new():
            return urlsafe_b64encode(urandom(8)).decode('utf-8').replace('=', '')

        if not slug:
            slug = _get_new()
        for i in range(10):
            if not ShortURL.objects.filter(slug=slug).exists():
                return slug
            slug = _get_new()
        return _get_new()


class ShortURLManager(Manager):
    def create(self, *args, **validated_data):
        validated_data['slug'] = _get_new_slug(validated_data.get('slug', ''))
        return super().create(*args, **validated_data)


class ShortURL(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=64, blank=True, unique=True)
    counter = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    url = models.URLField(default='')

    objects = ShortURLManager()

    @staticmethod
    def get(slug: str) -> 'ShortURL':
        if not slug:
            return
        result = ShortURL.objects.filter(slug=slug)
        if result.count():
            return result[0]

    def update_counter(self):
        self.counter += 1
        self.save()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.slug:
            self.slug = _get_new_slug()
        super().save(force_insert, force_update, using, update_fields)