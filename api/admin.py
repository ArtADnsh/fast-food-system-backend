from django.contrib import admin
from .models import Restaurant, MenuItem, Orders, OrderItem

# شخصی‌سازی ظاهر جدول رستوران‌ها در پنل ادمین
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant_id', 'name', 'rating_avg', 'delivery_fee', 'total_orders')
    search_fields = ('name', 'phone')
    list_filter = ('rating_avg',)

# شخصی‌سازی جدول غذاها
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'category', 'price')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('category', 'restaurant')

# یک ترفند حرفه‌ای: نمایش آیتم‌های هر سفارش دقیقاً داخل صفحه همان سفارش
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# شخصی‌سازی جدول سفارشات
@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__user_id',)
    inlines = [OrderItemInline] # اضافه کردن ریزفاکتور به صفحه سفارش