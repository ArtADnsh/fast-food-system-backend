from rest_framework import serializers
from .models import Restaurant, MenuItem, Category


class RestaurantSerializer(serializers.ModelSerializer):
    # Mapping the database fields to match the keys your frontend expects
    id = serializers.IntegerField(source='restaurant_id', read_only=True)
    rating = serializers.DecimalField(source='rating_avg', max_digits=2, decimal_places=1, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'rating', 'delivery_fee']


class MenuItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='item_id', read_only=True)
    # Flattens the category relationship to just return the string name (e.g., "Pizza")
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category']