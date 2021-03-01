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
        fields = '__all__'


class SDSPDFSerializer(serializers.ModelSerializer):
    language = serializers.CharField(max_length=100)
    manufacturer = serializers.CharField(max_length=100)

    class Meta:
        model = SDS_PDF
        fields = '__all__'

    def validate(self, attr):
        attr['pdf_md5'] = md5hash(attr['sds_product_name'], attr['sds_harvest_source'])
        attr['sds_download_url'] = f"{settings.MACHINE_URL}:8080/media/sds/{attr['sds_harvest_source'].id}" \
                                   f"/sds/{attr['name']}".replace(' ', '%20')
        attr['language'] = Language.objects.get(name=attr['language'])
        attr['manufacturer'] = Manufacturer.objects.get(name=attr['manufacturer'])

        return attr

    def create(self, validated_data):
        instance = SDS_PDF.objects.filter(pdf_md5=validated_data['pdf_md5'])

        if instance.exists():
            instance = self.update(instance[0], validated_data)
        else:
            instance = super().create(validated_data)

        product, _ = Product.objects.get_or_create(sds_pdf=instance,
                                                   defaults={'name': instance.sds_product_name,
                                                             'language': instance.language})
        if not _ and product.name != instance.sds_product_name:
            product.name = instance.sds_product_name

        product.save()
        return instance


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
