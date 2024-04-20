from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from . custom_fields import TenDigitBigIntegerField
from django.utils import timezone
from django.core.exceptions import ValidationError
import hashlib
CATEGORY_CHOICES = (
    ('BU','Bullet'),
    ('DO','Dome'),
    ('TU','Turret')
)

STATES = (
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal')
)

class product(models.Model):
    title= models.CharField(max_length=100)
    selling_price= models.IntegerField()
    description = models.TextField()
  #  catagory = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    image = models.ImageField(upload_to='product')
    image_hash = models.CharField(max_length=32, unique=True, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.image_hash:
            self.image_hash = self.generate_image_hash(self.image)
        super(Gallery, self).save(*args, **kwargs)

    @staticmethod
    def generate_image_hash(image):
        hash_object = hashlib.md5()
        for chunk in image.chunks():
            hash_object.update(chunk)
        return hash_object.hexdigest()
    
class customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=500)
    mobile = TenDigitBigIntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATES,max_length=200)
    def __str__(self):
        return self.name
class faq(models.Model):
    q = models.CharField(max_length=200)
    ans = models.CharField(max_length=500)
    def __str__(self):
        return self.q
    
class faqsection(models.Model):
    q = models.CharField(max_length=200)
    ans = models.CharField(max_length=1000)
    def __str__(self):
        return self.q

class cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

class UserLoginStat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    session_id = models.CharField(max_length=100,default=None,null=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

def get_local_time():
    return timezone.localtime(timezone.now())

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=get_local_time)

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class Payment(models.Model):
        user = models.ForeignKey(User,on_delete=models.CASCADE)
        amount = models.FloatField()
        razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
        razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
        razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
        paid = models.BooleanField(default=False)

class Orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default='')
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price