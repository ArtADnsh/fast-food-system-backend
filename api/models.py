# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    address_id = models.AutoField(db_column='Address_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=255, blank=True, null=True)  # Field name made lowercase.
    zipcode = models.CharField(db_column='Zipcode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    is_verified = models.IntegerField(db_column='Is_Verified', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ADDRESS'


class Category(models.Model):
    category_id = models.AutoField(db_column='Category_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CATEGORY'


class Employee(models.Model):
    employee_id = models.AutoField(db_column='Employee_ID', primary_key=True)  # Field name made lowercase.
    ssn = models.CharField(db_column='SSN', unique=True, max_length=20)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=10, blank=True, null=True)  # Field name made lowercase.
    salary = models.DecimalField(db_column='Salary', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    employed_date = models.DateField(db_column='Employed_Date', blank=True, null=True)  # Field name made lowercase.
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='Restaurant_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EMPLOYEE'


class MenuItem(models.Model):
    item_id = models.AutoField(db_column='Item_ID', primary_key=True)  # Field name made lowercase.
    restaurant = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='Restaurant_ID')  # Field name made lowercase.
    category = models.ForeignKey(Category, models.DO_NOTHING, db_column='Category_ID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MENU_ITEM'


class Orders(models.Model):
    order_id = models.AutoField(db_column='Order_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    address = models.ForeignKey(Address, models.DO_NOTHING, db_column='Address_ID', blank=True, null=True)  # Field name made lowercase.
    delivery_staff = models.ForeignKey('Staff', models.DO_NOTHING, db_column='Delivery_Staff_ID', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=50)  # Field name made lowercase.
    preparation_status = models.CharField(db_column='Preparation_Status', max_length=9, blank=True, null=True)  # Field name made lowercase.
    total_price = models.DecimalField(db_column='Total_Price', max_digits=10, decimal_places=2)  # Field name made lowercase.
    estimated_delivery = models.DateTimeField(db_column='Estimated_Delivery', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_At', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ORDERS'


class OrderItem(models.Model):
    orderitem_id = models.AutoField(db_column='OrderItem_ID', primary_key=True)  # Field name made lowercase.
    order = models.ForeignKey(Orders, models.DO_NOTHING, db_column='Order_ID')  # Field name made lowercase.
    item = models.ForeignKey(MenuItem, models.DO_NOTHING, db_column='Item_ID')  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    unit_price = models.DecimalField(db_column='Unit_Price', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ORDER_ITEM'


class Payment(models.Model):
    payment_id = models.AutoField(db_column='Payment_ID', primary_key=True)  # Field name made lowercase.
    order = models.OneToOneField(Orders, models.DO_NOTHING, db_column='Order_ID')  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=50)  # Field name made lowercase.
    transaction_id = models.CharField(db_column='Transaction_ID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    paid_at = models.DateTimeField(db_column='Paid_At', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PAYMENT'


class Restaurant(models.Model):
    restaurant_id = models.AutoField(db_column='Restaurant_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    rating_avg = models.DecimalField(db_column='Rating_Avg', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    opening_hour = models.TimeField(db_column='Opening_Hour', blank=True, null=True)  # Field name made lowercase.
    closing_hour = models.TimeField(db_column='Closing_Hour', blank=True, null=True)  # Field name made lowercase.
    delivery_fee = models.DecimalField(db_column='Delivery_Fee', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    is_active = models.IntegerField(db_column='Is_Active', blank=True, null=True)  # Field name made lowercase.
    total_orders = models.IntegerField(db_column='Total_Orders', blank=True, null=True)  # Field name made lowercase.
    total_revenue = models.DecimalField(db_column='Total_Revenue', max_digits=12, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESTAURANT'


class RestaurantAdmin(models.Model):
    admin = models.OneToOneField(Employee, models.DO_NOTHING, db_column='Admin_ID', primary_key=True)  # Field name made lowercase.
    permission = models.CharField(db_column='Permission', max_length=255, blank=True, null=True)  # Field name made lowercase.
    restaurant = models.ForeignKey(Restaurant, models.DO_NOTHING, db_column='Restaurant_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RESTAURANT_ADMIN'


class Review(models.Model):
    review_id = models.AutoField(db_column='Review_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    restaurant = models.ForeignKey(Restaurant, models.DO_NOTHING, db_column='Restaurant_ID', blank=True, null=True)  # Field name made lowercase.
    item = models.ForeignKey(MenuItem, models.DO_NOTHING, db_column='Item_ID', blank=True, null=True)  # Field name made lowercase.
    staff = models.ForeignKey('Staff', models.DO_NOTHING, db_column='Staff_ID', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(db_column='Created_At', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'REVIEW'


class Staff(models.Model):
    staff = models.OneToOneField(Employee, models.DO_NOTHING, db_column='Staff_ID', primary_key=True)  # Field name made lowercase.
    avg_rating = models.DecimalField(db_column='Avg_Rating', max_digits=2, decimal_places=1, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=14)  # Field name made lowercase.
    approval_status = models.CharField(db_column='Approval_Status', max_length=8, blank=True, null=True)  # Field name made lowercase.
    restaurant = models.ForeignKey(Restaurant, models.DO_NOTHING, db_column='Restaurant_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'STAFF'


class Users(models.Model):
    user_id = models.AutoField(db_column='User_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', unique=True, max_length=20)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    registration_date = models.DateTimeField(db_column='Registration_Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USERS'