from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from serializers.user import UserSerializer


class UserView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context={'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            form.instance.is_active = True
            form.instance.is_staff = True
            form.save()
            return redirect(reverse(''))
        else:
            print(form.errors)
            print("Form is not valid")
            return render(request, template_name="index.html", context={'form': form})
