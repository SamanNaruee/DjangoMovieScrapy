from .models import Laptop
from rest_framework import serializers

class LoptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = '__all__'
        read_only_fields = ['id', 'source_url']