from django.urls import path
from rest_framework_nested import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet , basename='userviewset')
# router.register(r'register', RegisterView , basename='registerview')
router.register(r'teams', TeamViewSet, basename='teamviewset')

# router.register(r'auth', TokenObtainPairView as viewset, basename='token_obtain_pair')  # This line is incorrect

# TokenObtainPairView and TokenRefreshView are APIViews (not ViewSets).
# Register them as explicit URL patterns instead of router.register.

urlpatterns = router.urls