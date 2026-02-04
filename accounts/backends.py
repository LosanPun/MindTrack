# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows login with either username or email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        
        if username is None:
            username = kwargs.get('username')
        
        try:
            # Try to find user by username OR email
            user = UserModel.objects.get(
                Q(username__iexact=username) | 
                Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # User doesn't exist
            return None
        except UserModel.MultipleObjectsReturned:
            # Multiple users found (shouldn't happen with unique constraints)
            user = UserModel.objects.filter(
                Q(username__iexact=username) | 
                Q(email__iexact=username)
            ).first()
        
        # Check password
        if user and user.check_password(password):
            return user
        return None
    
    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None