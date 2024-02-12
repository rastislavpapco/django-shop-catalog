from rest_framework import serializers

import catalog.models as models


class AttributeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeName
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeValue
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attribute
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductAttributes
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = '__all__'


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Catalog
        fields = '__all__'
