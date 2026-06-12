import jwt
import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView

from .authentication import CustomJWTAuthentication
from .models import Restaurant, MenuItem, Category, Users
from .serializers import RestaurantSerializer, MenuItemSerializer, UsersSerializer
from .permissions import IsValidUser


# ==========================================
#   Restaurant List View
# ==========================================
class RestaurantListView(generics.ListAPIView):
    """
    API for listing restaurants.
    """
    queryset = Restaurant.objects.filter(is_active=1)
    serializer_class = RestaurantSerializer


# ==========================================
# 2. Restaurant Menu Retrieve View
# ==========================================
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
                "delivery_fee": restaurant.delivery_fee
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