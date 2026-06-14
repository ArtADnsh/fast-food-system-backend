from rest_framework import serializers
from .models import Restaurant, MenuItem, Category, Users, Orders, OrderItem, Staff, Review


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

    has_review = serializers.SerializerMethodField()
    review_data = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = '__all__'

    def get_has_review(self, obj):
        return Review.objects.filter(order=obj).exists()

    def get_review_data(self, obj):
        review = Review.objects.filter(order=obj).first()
        if review:
            return {
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at
            }
        return None


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['status', 'preparation_status', 'delivery_staff']

    def validate(self, attrs):
        staff = attrs.get('delivery_staff')
        # اگر درخواستی برای تغییر پیک داشتیم
        if staff:
            # چک کردن اینکه نقش حتما DeliveryPerson باشه
            if staff.role != 'DeliveryPerson':
                raise serializers.ValidationError("این کارمند مجاز به تحویل سفارش نیست (نقش او DeliveryPerson نیست).")
        return attrs


class StaffListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='staff.name') # دسترسی به نام از طریق Employee که با Staff در ارتباطه
    class Meta:
        model = Staff
        fields = ['staff_id', 'name', 'role']

class OrderSerializer(serializers.ModelSerializer):
    has_review = serializers.SerializerMethodField()
    review_data = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.name', read_only=True)
    address_str = serializers.CharField(source='address.street', read_only=True)

    class Meta:
        model = Orders
        fields = '__all__' # چون فقط برای مشاهده است، همه فیلدها را برمی‌گردانیم

    def get_has_review(self, obj):
        # بررسی می‌کنیم آیا رکوردی در جدول Review برای این سفارش هست یا نه
        return Review.objects.filter(order=obj).exists()

    def get_review_data(self, obj):
        # اگر نظر داشت، اطلاعاتش را هم می‌فرستیم تا کاربر بتواند آن را ببیند
        review = Review.objects.filter(order=obj).first()
        if review:
            return {
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at
            }
        return None


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['order', 'rating', 'comment']

    def validate(self, attrs):
        order = attrs.get('order')
        # این همان رکوردی است که CustomJWTAuthentication شما توی request می‌گذارد (از جنس مدل Users خودت)
        user = self.context['request'].user

        if order.user != user:
            raise serializers.ValidationError("شما فقط می‌توانید برای سفارشات خودتان نظر ثبت کنید.")

        # بررسی وضعیت تحویل
        if order.status != 'Delivered':
            raise serializers.ValidationError("فقط برای سفارشاتی که تحویل داده شده‌اند امکان ثبت نظر وجود دارد.")

        # جلوگیری از ثبت نظر تکراری
        if Review.objects.filter(order=order).exists():
            raise serializers.ValidationError("شما قبلاً برای این سفارش نظر خود را ثبت کرده‌اید.")

        return attrs