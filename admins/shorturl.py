from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import forms
from django.urls import reverse

from models.models import ShortURL

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ["title", "counter", "slug", "url"]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        disabled_fields = ["counter"]
        if not request.user.is_superuser:
            disabled_fields.extend(["slug", "user", "counter"])

        for f in disabled_fields:
            if f in form.base_fields:
                del form.base_fields[f]
        # print(dir(form))
        # print(dir(form.base_fields['slug']))
        return form

    def save_form(self, request, form, change):
        from django.forms import fields, models
        print("FORM", dir(form))
        print(form.cleaned_data)
        print(form.instance)
        form.instance.user = request.user
        return super().save_form(request, form, change)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

    def slug(self, instance):
        return reverse("index_view", kwargs=instance.slug)

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True


admin.site.register(ShortURL, ShortURLAdmin)