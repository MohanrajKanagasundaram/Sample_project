from django.urls import path
from evaluation_app.api.views import PredictionView,MetricsView

urlpatterns = [
    path('data/',PredictionView,name='Predictions'),
    path('metrics/',MetricsView,name='Performance Metrics'),
]