from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import UserLoginStat

@receiver(user_logged_in)
def user_login(sender, request, user, **kwargs):
    login_record = UserLoginStat(
        user=user,
        login_time=timezone.now(),
        ip_address=request.META.get('REMOTE_ADDR'),
        session_id=request.session.session_key
    )
    login_record.save()

@receiver(user_logged_out)
def user_logout(sender, request, user, **kwargs):
    try:
        last_login_record = UserLoginStat.objects.filter(user=user).latest('login_time')
        last_login_record.logout_time = timezone.now()
        last_login_record.save()
    except UserLoginStat.DoesNotExist:
        pass
