#from django.contrib.auth.models import AbstractUser
#from django.db import models

#class CustomUser(AbstractUser):
    # We'll add custom fields later
#    free_analyses_used = models.IntegerField(default=0)
#    is_premium = models.BooleanField(default=False)
    
#    def can_analyze_free(self):
#        return self.free_analyses_used < 3
    
#    def __str__(self):
#        return self.email