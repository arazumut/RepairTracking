from rest_framework import serializers
from .models import Musteri, Arac, IsEmri

class MusteriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Musteri
        fields = '__all__'

class AracSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arac
        fields = '__all__'

class IsEmriSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsEmri
        fields = '__all__'
