import jwt
import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
from django.db import transaction
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

from .authentication import CustomJWTAuthentication
from .models import Restaurant, MenuItem, Category, Users, OrderItem, Orders
from .serializers import RestaurantSerializer, MenuItemSerializer, UsersSerializer, OrdersSerializer
from .permissions import IsValidUser
from .filters import RestaurantFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RestaurantListView(generics.ListAPIView):
    """
    API for listing restaurants.
    """
    queryset = Restaurant.objects.filter(is_active=1)
    serializer_class = RestaurantSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        filters.DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    # اتصال کلاس فیلتر
    filterset_class = RestaurantFilter

    # فیلدهای سرچ متنی
    search_fields = ['name']

    # فیلدهای مجاز برای مرتب‌سازی (Sorting)
    ordering_fields = ['rating_avg', 'delivery_fee', 'total_orders']


class RestaurantMenuRetrieveView(generics.RetrieveAPIView):
    """
    API for restaurant info and menu
    """
    queryset = Restaurant.objects.filter(is_active=1)
    serializer_class = RestaurantSerializer  # برای نمایش در Browsable API

    def retrieve(self, request, *args, **kwargs):
        # متد get_object به صورت خودکار رستوران را پیدا کرده
        # و در صورت عدم وجود، ارور 404 استاندارد برمی‌گرداند
        restaurant = self.get_object()

        # دریافت تمام آیتم‌های منو برای این رستوران
        items = MenuItem.objects.filter(restaurant_id=restaurant.restaurant_id)

        # استخراج دسته‌بندی‌های یکتا از این آیتم‌ها
        category_ids = items.values_list('category_id', flat=True).distinct()
        categories = Category.objects.filter(category_id__in=category_ids).values_list('name', flat=True)

        # سریالایز کردن آیتم‌های منو
        item_serializer = MenuItemSerializer(items, many=True)

        # ساخت و بازگرداندن ساختار JSON اختصاصی برای فرانت‌اند
        return Response({
            "restaurant": {
                "id": restaurant.restaurant_id,
                "name": restaurant.name,
                "rating": restaurant.rating_avg,
                "delivery_fee": restaurant.delivery_fee,
                "address": restaurant.address,
                "phone": restaurant.phone,
                "opening_hour": restaurant.opening_hour,
                "closing_hour": restaurant.closing_hour,
                "total_orders": restaurant.total_orders
            },
            "categories": list(categories),
            "items": item_serializer.data
        })

class LoginAPIView(APIView):
    """
    API for user authentication and JWT generation.
    """

    def post(self, request, *args, **kwargs):
        username_input = request.data.get('username')
        password_input = request.data.get('password')

        if not username_input or not password_input:
            return Response(
                {"error": "لطفا نام کاربری و رمز عبور را وارد کنید"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check database for matching phone OR email
        user = Users.objects.filter(phone=username_input).first()
        if not user:
            user = Users.objects.filter(email=username_input).first()

        # Verify user exists and password matches (using plain text as per SQL seed data)
        if user and user.password == password_input:
            # Create the JWT Payload
            payload = {
                'user_id': user.user_id,
                'phone': user.phone,
                'name': user.name,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'iat': datetime.datetime.utcnow()
            }

            # Encode the token
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({
                "access_token": token,
                "user_info": {
                    "name": user.name,
                    "phone": user.phone
                }
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "نام کاربری یا رمز عبور اشتباه است"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class RegisterAPIView(generics.CreateAPIView):
    """
    API for registering a new user.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    CBV for retrieving and updating the logged-in user's profile.
    """
    serializer_class = UsersSerializer
    authentication_classes = [CustomJWTAuthentication] # Apply our custom Auth
    permission_classes = [IsValidUser]                 # Apply our custom Permission

    def get_object(self):
        # Because of our authentication class, request.user is our MySQL user object!
        # This ensures users can ONLY retrieve/edit their own profile.
        return self.request.user


class CheckoutAPIView(APIView):
    """
    CBV for processing a user's cart and creating an order in the database.
    """
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsValidUser]

    @transaction.atomic  # Ensures both Order and OrderItems are saved safely together
    def post(self, request, *args, **kwargs):
        user = request.user
        cart_items = request.data.get('cart', [])

        if not cart_items:
            return Response({"error": "سبد خرید شما خالی است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Calculate the real total price securely from the database
            subtotal = 0

            first_item_in_cart = MenuItem.objects.get(item_id=cart_items[0]['id'])
            delivery_fee = first_item_in_cart.restaurant.delivery_fee

            for item in cart_items:
                menu_item = MenuItem.objects.get(item_id=item['id'])
                subtotal += (menu_item.price * item['quantity'])

            total_price = subtotal + delivery_fee

            # 2. Create the main Order record
            order = Orders.objects.create(
                user=user,
                status='Pending',
                preparation_status='Pending',
                total_price=total_price,
                created_at=datetime.datetime.now()
            )

            # 3. Create the individual Order Items
            for item in cart_items:
                if item.get('quantity', 0) <= 0:
                    return Response(
                        {"error": "تعداد نامعتبر است."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                menu_item = MenuItem.objects.get(item_id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    item=menu_item,
                    quantity=item['quantity'],
                    unit_price=menu_item.price
                )

            return Response({
                "message": "سفارش با موفقیت ثبت شد!",
                "order_id": order.order_id
            }, status=status.HTTP_201_CREATED)

        except MenuItem.DoesNotExist:
            return Response({"error": "یکی از آیتم‌های سبد خرید در منو یافت نشد."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderHistoryAPIView(generics.ListAPIView):
    """
    API endpoint to fetch the logged-in user's order history.
    """
    serializer_class = OrdersSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsValidUser]

    def get_queryset(self):
        # request.user is set by our CustomJWTAuthentication class
        # order_by('-created_at') ensures the newest orders show up first
        return Orders.objects.filter(user=self.request.user).order_by('-created_at')