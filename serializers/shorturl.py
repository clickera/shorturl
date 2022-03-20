from rest_framework import serializers

from models.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ShortURL
        fields = '__all__'
