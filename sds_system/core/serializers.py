from rest_framework import serializers

from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.CharField(max_length=100)
    language = serializers.CharField(max_length=100)
    hash = serializers.SerializerMethodField()

    class Meta:
        model = Product
        depth = 1
        fields = '__all__'

    def validate(self, attr):
        attr['language'] = Language.objects.get(name=attr['language'])
        attr['provider'] = Provider.objects.get(name=attr['provider'])
        return attr

    @staticmethod
    def get_hash(obj):
        hashed = str(obj.provider.name) + '-' + str(obj.sds_pdf_product_name)
        return hashlib.md5(hashed.encode()).hexdigest()


class ProducerOfSDSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProducerOfSDS
        fields = '__all__'


class SDSSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDS
        fields = '__all__'
