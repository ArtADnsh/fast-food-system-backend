import jwt
from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from .models import Employee, RestaurantAdmin


class RestaurantAdminMixin:
    """
    میکسین برای احراز هویت ادمین و دریافت رستوران او
    """
    def get_restaurant(self):
        auth_header = self.request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied("توکن معتبر ارسال نشده است.")

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            current_user_id = payload.get('user_id')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise PermissionDenied("توکن شما نامعتبر یا منقضی شده است.")

        if not current_user_id:
            raise PermissionDenied("آیدی کاربر در توکن یافت نشد.")

        # پیدا کردن ادمین بر اساس یوزر آیدی که از توکن استخراج شد
        # (با استفاده از Relationship بین Employee و RestaurantAdmin)
        admin_record = RestaurantAdmin.objects.filter(admin__user_id=current_user_id).first()

        if not admin_record or not admin_record.restaurant:
            raise PermissionDenied("شما دسترسی ادمین برای هیچ رستورانی ندارید.")

        return admin_record.restaurant