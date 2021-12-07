from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from PIL import Image
import decimal
from SAAS.models import Shop
# Create your models here.


class Customer(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=255)
    customer_email = models.EmailField(unique=True)
    customer_add = models.TextField()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.customer_email


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255, unique=True)
    vendor_picture = models.ImageField(upload_to="images/")
    tax_id = models.IntegerField(null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.vendor_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=255, unique=True)
    # brand_img = models.ImageField(upload_to="images/")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.category_name


class SellingType(models.Model):
    type_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.type_name


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    buying_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    stock_amount = models.PositiveIntegerField(default=0)
    out_of_stock = models.BooleanField(default=False, null=True, blank=True)
    item_img = models.ImageField(upload_to="images/", null=True)
    product_descriptions = models.TextField(null=True)
    upc = models.IntegerField(null=True, blank=True)
    sku = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.item_name)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

        if not self.item_img:
            return

        imag = Image.open(self.item_img.path)
        if imag.width > 400 or imag.height > 400:
            output_size = (400, 400)
            imag.thumbnail(output_size)
            imag.save(self.item_img.path)

    @property
    def get_items_by_category(self):
        return Item.objects.filter(category__item_name=self.title)

    @staticmethod
    def get_items(ids):
        return Item.objects.filter(id__in=ids)


class Table(models.Model):
    table_name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.table_name


class TableItems(models.Model):
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


class CartItems(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-id"]


class TableCheckout(models.Model):
    STATUS_CHOICES = (
        ("PAID", "PAID"),
        ("UNPAID", "UNPAID")
    )
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    item_item = models.ManyToManyField(TableItems)
    table_status = models.CharField(max_length=255, null=True)
    discount = models.FloatField(null=True)
    amount_received = models.DecimalField(
        decimal_places=2, max_digits=10, default=0.00)
    change = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # self.change = self.amount_received - 
        if float(self.total) > float(self.amount_received):
                self.change = decimal.Decimal(self.total) - decimal.Decimal(self.amount_received)
        else:
            self.change = decimal.Decimal(self.amount_received) - decimal.Decimal(self.total)
        if self.discount:
                discount = float(self.total) * float(self.discount) / 100
                self.total = float(self.total) - discount
        super(RestCheckout, self).save(*args, **kwargs)

class RestCheckout(models.Model):
    STATUS_CHOICE = (
        ("PAID", "PAID"),
        ("UNPAID", "UNPAID")
    )
    PAYMENT_CHOICE = (
        ("CASH", "CASH"),
        ("Credit Card", "Credit Card"),
        ("bKash", "bKash"),
        ("Nagad", "Nagad")
    )
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(CartItems)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    grand_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    amount_received = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    change = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    status = models.CharField(max_length=255, null=True, choices=STATUS_CHOICE)
    payment_method = models.CharField(max_length=120, null=True, choices=PAYMENT_CHOICE, default="CASH")
    payment_number = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        ordering = ["-id"]
    

    def __str__(self):
        return str(self.customer)
    
    def get_grand_total(self):
        return self.quantity * self.grand_total
    
    def save(self, *args, **kwargs):
        # self.change = self.amount_received - 
        if float(self.grand_total) > float(self.amount_received):
            self.change = decimal.Decimal(self.grand_total) - decimal.Decimal(self.amount_received)
        else:
            self.change = decimal.Decimal(self.amount_received) - decimal.Decimal(self.grand_total)
        if self.discount:
            discount = float(self.grand_total) * float(self.discount) / 100
            self.grand_total = float(self.grand_total) - discount
        super(RestCheckout, self).save(*args, **kwargs)


class DueModel(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_note = models.TextField()
    submission_date = models.DateField()
    items = models.ManyToManyField(CartItems)
    due_total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.customer.customer_email
