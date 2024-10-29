from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FileUploadViewSet

router = DefaultRouter()
router.register(r"upload", FileUploadViewSet, basename="upload")


urlpatterns = [
    path('', include(router.urls))
]