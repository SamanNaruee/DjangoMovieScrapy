from .models import Loptop
from rest_framework import serializers

class LoptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loptop
        fields = '__all__'
        read_only_fields = ['id', 'source_url']