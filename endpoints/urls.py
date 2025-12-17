from django.urls import path
from .views import health_check, analyze_crop

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('analyze-crop/', analyze_crop, name='analyze_crop'),
]