from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print("DDD", validated_data)
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = '__all__'