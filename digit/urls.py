from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import DigitRecognitionAPI

router = DefaultRouter()

router.register("recognition", DigitRecognitionAPI, basename="digit_recognition")

urlpatterns = []
urlpatterns += router.urls
