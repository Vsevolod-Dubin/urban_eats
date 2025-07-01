#menu/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Dish, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Dish
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    dishes = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)