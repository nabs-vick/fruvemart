from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField( max_length=10)
    email =models.EmailField(max_length=254)
    password = models.CharField( max_length=50)
    
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description =models.CharField(max_length=2000,default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/', height_field=None, width_field=None, max_length=None)
    
    is_fruit = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    address = models.CharField(default='', max_length=50,blank=True)
    phone = models.CharField(max_length=20,default='')
    date = models.DateField(default=datetime.datetime.today, auto_now=False, auto_now_add=False)
    status =models.BooleanField(default = False)
    
    def __str__(self):
        return self.product
    
    
class Feedback(models.Model):
    name = models.CharField( max_length=50)
    email = models.EmailField(max_length=254)
    message = models.CharField(max_length=250)
    def __str__(self):
        return self.name


class Cart_components(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    product_name = models.CharField( max_length=50)
    product_img = models.ImageField(upload_to='media/cart', height_field=None, width_field=None, max_length=None)
    address = models.CharField( max_length=100)
    town = models.CharField( max_length=50)
    phone_num = models.CharField( max_length=15)
    price = models.DecimalField( max_digits=6, decimal_places=2)
    message = models.CharField(max_length=250)
    def __str__(self):
        return f'{self.product_name} this is a product for {self.name}'
