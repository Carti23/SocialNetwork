from django.db import models
from django.contrib.auth.models import User
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.urls import reverse

# Post Model
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    liked_by = models.ManyToManyField(User,
                                      related_name='liked')
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


# password_reset function
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        "admin@gmail.com",
        # to:
        [reset_password_token.user.email]
    )