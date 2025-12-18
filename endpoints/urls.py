from django.urls import path
from .views import health_check, analyze_crop, diagnose_plant

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('analyze-crop/', analyze_crop, name='analyze_crop'),
    path('diagnose/', diagnose_plant, name='diagnose_plant'),
]