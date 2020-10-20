from rest_framework import serializers

from .models import *

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password')


class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Manufacturer
        fields = '__all__'


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProducerOfSDSSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProducerOfSDS
        fields = '__all__'


class SDSSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SDS
        fields = '__all__'
