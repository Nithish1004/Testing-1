from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('freelancer', 'Freelancer'),
        ('business', 'Business'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, null=True, blank=True)

    def get_freelancer(self):
        return getattr(self, 'freelancer', None)

    def get_business(self):
        return getattr(self, 'business', None)

    def __str__(self):
        return self.username

# class Freelancer(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='accounts_freelancer'
#     )
#     skills = models.CharField(max_length=255, blank=True)
#     bio = models.TextField(blank=True)
#     profile_pic = models.ImageField(upload_to='freelancer_profiles/', blank=True, null=True)
        
#     def __str__(self):
#         return self.user.username
    
# class Freelancer(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='accounts_freelancer'
#     )
#     name = models.CharField(max_length=255)
#     profile_pic = models.ImageField(upload_to='freelancer_profiles/', blank=True, null=True)
#     tagline = models.CharField(max_length=255, blank=True)
#     # skills = models.CharField(max_length=255, blank=True)
#     bio = models.TextField(blank=True)
#     website = models.URLField(blank=True)

#     def __str__(self):
#         return self.user.username

# class Business(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='accounts_business'
#     )
#     # company_name = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     # description = models.TextField(blank=True)
#     profile_pic = models.ImageField(upload_to='business_profiles/', blank=True, null=True)
#     bio = models.TextField(blank=True)

#     def __str__(self):
#         return self.user.username

