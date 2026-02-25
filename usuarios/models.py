from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

# Create profile automatically when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Forzar a que todos los usuarios sean staff (administradores)
        if not instance.is_staff:
            instance.is_staff = True
            instance.save()
            
        if not getattr(instance, '_ignore_profile_signal', False):
            try:
                Profile.objects.get_or_create(user=instance)
            except Exception:
                pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'profile'):
            instance.profile.save()
    except Exception:
        pass
