from .models import Laptop, Phones
from rest_framework import serializers

class LoptopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laptop
        fields = '__all__'
        read_only_fields = ['id', 'source_url']
        
class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phones
        fields = '__all__'
        read_only_fields = ['id', 'source_url']
        