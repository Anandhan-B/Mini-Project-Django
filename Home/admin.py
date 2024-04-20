from django.contrib import admin
from . models import product,customer,Gallery,cart,UserLoginStat,Feedback,Payment,Orders,faqsection
from django.contrib import admin
from django import forms
admin.site.site_header = "VS Administration"


class ImageModelAdminForm(forms.ModelForm):
    class Meta:
        model = Gallery
        exclude = ('image_hash',)
        widgets = {'image_hash': forms.HiddenInput(),}

class ImageModelAdmin(admin.ModelAdmin):
    form = ImageModelAdminForm

admin.site.register(Gallery, ImageModelAdmin)

@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','content','timestamp']

@admin.register(product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','selling_price','product_image']

@admin.register(customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','mobile','state']

@admin.register(faqsection)
class FaqModelAdmin(admin.ModelAdmin):
    list_display = ['q','ans']

@admin.register(cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(Orders)

class OrdersModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']

@admin.register(UserLoginStat)

class UserLoginModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time' , 'ip_address', 'session_id')
    search_fields = ('user__username', 'ip_address','login_time', 'logout_time')