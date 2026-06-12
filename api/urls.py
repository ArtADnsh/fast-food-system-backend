from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListView.as_view(), name='get_restaurants'),
    path('restaurants/<int:pk>/menu/', views.RestaurantMenuRetrieveView.as_view(), name='get_restaurant_menu'),
]