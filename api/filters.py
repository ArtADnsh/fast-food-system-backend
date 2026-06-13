from django_filters import rest_framework as filters
from .models import Restaurant


class RestaurantFilter(filters.FilterSet):
    # جستجو برای نام شهر در داخل ستون آدرس
    city = filters.CharFilter(field_name='address', lookup_expr='icontains')

    # استفاده از نام صحیح: rating_avg
    min_rating = filters.NumberFilter(field_name='rating_avg', lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name='rating_avg', lookup_expr='lte')

    free_delivery = filters.BooleanFilter(method='filter_free_delivery')

    class Meta:
        model = Restaurant
        fields = ['city', 'min_rating', 'max_rating']

    def filter_free_delivery(self, queryset, name, value):
        if value:
            return queryset.filter(delivery_fee=0)
        return queryset