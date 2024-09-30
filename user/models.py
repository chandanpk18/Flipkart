from django.db import models
from django.contrib.auth.models import User

class ProductType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(ProductType, related_name='categories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.product_type.name})"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class HelpRequest(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Resolved', 'Resolved'),
    ]
    username = models.CharField(max_length=100)
    email = models.EmailField()
    help_text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')

    def __str__(self):
        return self.username