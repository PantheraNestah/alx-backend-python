# chats/auth.py

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# If you want to add custom claims to your JWT tokens
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # You could add other user-specific data here, e.g., 'is_admin': user.is_staff

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# If you create a custom serializer like MyTokenObtainPairSerializer,
# you would update SIMPLE_JWT settings in messaging_app/settings.py like this:
# SIMPLE_JWT = {
#     ...
#     "TOKEN_OBTAIN_SERIALIZER": "chats.auth.MyTokenObtainPairSerializer",
#     ...
# }