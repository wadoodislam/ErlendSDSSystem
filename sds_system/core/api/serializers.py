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
    language = serializers.CharField(max_length=100)
    sds_pdf = serializers.CharField(max_length=100)

    class Meta:
        model = Product
        # depth = 1
        fields = '__all__'

    # def validate(self, attr):
    #     attr['id'] = md5hash(attr['sds_product_name'], attr['provider'])
    #     attr['link'] = f"{settings.MACHINE_URL}:8080/media/sds/{attr['provider']}/sds/{attr['name']}".replace(' ', '%20')
    #     attr['language'] = Language.objects.get(name=attr['language'])
    #     attr['sds_harvest_source'] = SDSHarvestSource.objects.get(name=attr['sds_harvest_source'])
    #
    #     return attr
    #
    # def create(self, validated_data):
    #     instance = Product.objects.filter(id=validated_data['id'])
    #     if instance.exists():
    #         return self.update(instance[0], validated_data)
    #
    #     return super().create(validated_data)


class SDSPDFSerializer(serializers.ModelSerializer):
    language = serializers.CharField(max_length=100)
    manufacturer = serializers.CharField(max_length=100)
    sds_harvest_source = serializers.CharField(max_length=100)

    class Meta:
        model = SDS_PDF
        depth = 1
        fields = '__all__'

    def validate(self, attr):
        attr['pdf_md5'] = md5hash(attr['sds_product_name'], attr['sds_harvest_source'])
        attr['sds_download_url'] = f"{settings.MACHINE_URL}:8080/media/sds/{attr['sds_harvest_source']}/sds/{attr['name']}".replace(' ', '%20')
        attr['language'] = Language.objects.get(name=attr['language'])
        attr['manufacturer'] = Manufacturer.objects.get(name=attr['manufacturer'])
        attr['sds_harvest_source'] = SDSHarvestSource.objects.get(name=attr['sds_harvest_source'])
        attr['sds_harvest_run'] = SDSHarvestRun.objects.get(sds_harvest_source=attr['sds_harvest_source'])

        return attr

    def create(self, validated_data):
        instance = SDS_PDF.objects.filter(pdf_md5=validated_data['pdf_md5'])
        if instance.exists():
            return self.update(instance[0], validated_data)

        return super().create(validated_data)


class SDSHarvestSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SDSHarvestSource
        fields = '__all__'


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
