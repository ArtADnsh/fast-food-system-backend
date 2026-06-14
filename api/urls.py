from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListView.as_view(), name='get_restaurants'),
    path('restaurants/<int:pk>/menu/', views.RestaurantMenuRetrieveView.as_view(), name='get_restaurant_menu'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    path('checkout/', views.CheckoutAPIView.as_view(), name='api_checkout'),
    path('orders/', views.OrderHistoryAPIView.as_view(), name='api_orders_history'),
    path('restaurants/my-menu/', views.MyMenuAPIView.as_view(), name='my-menu-list'),
    path('restaurants/my-menu/<int:pk>/', views.MyMenuDetailAPIView.as_view(), name='my-menu-detail'),
    path('admin/orders/', views.OrderListAPIView.as_view(), name='order-list'),
    path('admin/orders/<int:pk>/', views.OrderUpdateAPIView.as_view(), name='order-update'),
    path('admin/delivery-staff/', views.DeliveryStaffListAPIView.as_view(), name='delivery-staff-list'),
]