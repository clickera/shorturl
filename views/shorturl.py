from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from models.models import ShortURL

from serializers.shorturl import ShortURLSerializer


class CabinetView(APIView):
    def get(self, request, slug: str):
        instance = ShortURL.get(slug)
        if not instance:
            return Response({"status": 404, "message": "Not found"}, status=404)
        instance.update_counter()
        return redirect(instance.url)


class ShortURLView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    pagination_class = PageNumberPagination

    def filter_queryset(self, queryset):
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)
