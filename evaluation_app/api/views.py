from rest_framework.decorators import api_view
from rest_framework.response import Response
from evaluation_app.models import Metrics
from evaluation_app.api.serializers import MetricSerializer


@api_view(['GET','POST','DELETE'])
def PredictionView(request):
    if(request.method == 'GET'):
       data=Metrics.objects.all()
       Resp=MetricSerializer(data,many=True) 
       return Response(Resp.data)
    elif(request.method=='POST'):
        serializer=MetricSerializer(data=request.data,many=True)
        if(serializer.is_valid()):
             serializer.save()
             return Response({'status':'success'})
        else:
           return  Response(serializer.errors)
    elif(request.method=='DELETE'):
        data=Metrics.objects.all()
        data.delete()
        return Response({'status':'success','message':'deleted all metrics'})
 
@api_view(['GET'])      
def MetricsView(request):
    if(request.method=='GET'):
        data=Metrics.objects.all()
        total=0
        tp=0
        for each in data:
            if each.field_type==each.pred:
                tp=tp+1
            total=total+1
        
        return Response({'accuracy':str(round((tp/total),4))})
    
    
    
        