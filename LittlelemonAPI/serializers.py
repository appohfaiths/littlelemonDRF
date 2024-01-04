from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import bleach
from .models import MenuItem, Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']


class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    # unique validation
    # title = serializers.CharField(max_length=255, validators=[
    #                               UniqueValidator(queryset=MenuItem.objects.all())])
    # validation using conditions in the field
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, min_value=2)
    # changing the name of a field using serializers
    # stock = serializers.IntegerField(source='inventory')
    # adding a new field using serializer methods
    # using validation method 1
    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError(
    #             'Price should not be less than 2.0')
    # using validation method 2
    def validate(self, attrs):
        # sanitizing data in validate method
        # attrs['title'] = bleach.clean(attrs['title'])
        if (attrs['price'] < 2):
            raise serializers.ValidationError(
                'Price should not be less than 2.36')
        if (attrs['inventory'] < 0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
    # sanitizing data

    def validate_title(self, value):
        return bleach.clean(value)
    price_after_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')
    # category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock',
                  'price_after_tax', 'category', 'category_id']
        extra_kwargs = {
            'stock': {'source': 'inventory', 'min_value': 0},
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItem.objects.all()
                    )
                ]
            }
        }
        depth = 1

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
