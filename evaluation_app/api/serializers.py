from rest_framework import serializers
from evaluation_app.models import Metrics


        

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model=Metrics
        fields='__all__'