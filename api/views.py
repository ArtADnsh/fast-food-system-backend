from rest_framework import generics
from rest_framework.response import Response
from .models import Restaurant, MenuItem, Category
from .serializers import RestaurantSerializer, MenuItemSerializer


# ==========================================
#   Restaurant List View
# ==========================================
class RestaurantListView(generics.ListAPIView):
    """
    لیست کردن تمام رستوران‌های فعال
    """
    queryset = Restaurant.objects.filter(is_active=1)
    serializer_class = RestaurantSerializer


# ==========================================
# 2. Restaurant Menu Retrieve View
# ==========================================
class RestaurantMenuRetrieveView(generics.RetrieveAPIView):
    """
    دریافت اطلاعات یک رستوران خاص به همراه دسته‌بندی‌ها و آیتم‌های منو
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