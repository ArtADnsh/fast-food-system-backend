from rest_framework import serializers
from .models import Restaurant, MenuItem, Category, Users, Orders, OrderItem


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


class UsersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user_id', read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'phone', 'password', 'registration_date']
        extra_kwargs = {
            'password': {'write_only': True},
            'registration_date': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    # We use source='item.name' to reach across the Foreign Key and grab the food's name
    item_name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity', 'unit_price']


class OrdersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='order_id', read_only=True)
    # This pulls all related items.
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'total_price', 'status', 'created_at', 'items']