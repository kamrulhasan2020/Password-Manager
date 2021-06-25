from rest_framework import serializers
from .models import Data


class DataSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Data
        fields = ['id', 'title', 'owner', 'login', 'password']
