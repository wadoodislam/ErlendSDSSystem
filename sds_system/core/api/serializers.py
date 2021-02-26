from django.conf import settings
from rest_framework import serializers

from core.models import *
from core.utils import md5hash

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(max_length=100)
    language = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        depth = 1
        fields = '__all__'

    def validate(self, attr):
        attr['id'] = md5hash(attr['sds_product_name'], attr['provider'])
        attr['link'] = f"{settings.MACHINE_URL}:8080/media/sds/{attr['provider']}/sds/{attr['name']}".replace(' ', '%20')
        attr['language'] = Language.objects.get(name=attr['language'])
        attr['sds_harvest_source'] = SDSHarvestSource.objects.get(name=attr['sds_harvest_source'])

        return attr

    def create(self, validated_data):
        instance = Product.objects.filter(id=validated_data['id'])
        if instance.exists():
            return self.update(instance[0], validated_data)

        return super().create(validated_data)


class ProducerOfSDSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerOfSDS
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class SDSHarvestSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDSHarvestSource
        fields = '__all__'
