from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from procedure_app.models import Procedure,Section,Field
from procedure_app.api.serializers import ProcedureSerializer,SectionSerializer,FieldSerializer
from procedure_app.api.paginations import ProcedurePagination

from django.template import RequestContext


# def handler404(request, *args, **argv):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request, *args, **argv):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response
def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'404.json', data)

class ProcedureView(generics.CreateAPIView,generics.ListAPIView,generics.DestroyAPIView,generics.UpdateAPIView):
    serializer_class=ProcedureSerializer
    pagination_class=ProcedurePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        if(pk!=None):
            query_set=Procedure.objects.filter(pk=pk)
            if not(query_set.exists()):
                res = serializers.ValidationError({'staus':'False','message':'Give valid procedure id'})
                res.status_code = 200
                raise res
            else:
                return query_set
        else:
            return Procedure.objects.all()
    def perform_destroy(self,instance):
        pk=self.kwargs.get('pk')
        id=Procedure.objects.get(pk=pk)
        id.delete()
class SectionView(generics.CreateAPIView,generics.ListAPIView,generics.DestroyAPIView,generics.UpdateAPIView):
    serializer_class=SectionSerializer
    queryset=Section.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name']
    def perform_destroy(self,instance):
        pk=self.kwargs.get('pk')
        id=Section.objects.get(pk=pk)
        id.delete()
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        procedure=self.request.query_params.get('procedure')
        if(pk!=None):
            query_set=Section.objects.filter(pk=pk)
            if not(query_set.exists()):
                raise ValidationError("Section not exists")
            else:
                return query_set
        elif(procedure!=None):
            query_set=Section.objects.filter(procedure=procedure)
            if not(query_set.exists()):
                res = serializers.ValidationError({'staus':'False','message':'Give valid procedure id'})
                res.status_code = 200
                raise res
            else:
                return query_set
        else:
            return Section.objects.all()
class FieldView(generics.CreateAPIView,generics.ListAPIView,generics.DestroyAPIView,generics.UpdateAPIView):
    serializer_class=FieldSerializer
    queryset=Field.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['label']

    def perform_destroy(self,instance):
        pk=self.kwargs.get('pk')
        id=Field.objects.get(pk=pk)
        id.delete()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "status":"success"
        },
        status=status.HTTP_200_OK)
    def get_queryset(self):
        section=self.request.query_params.get('section')
        query_set=Field.objects.filter(section=section)
        if not(query_set.exists()):
             res = serializers.ValidationError({'staus':'False','message':'Give valid section id'})
             res.status_code = 200
             raise res
            
        else:
            return query_set

class FieldViewSet(viewsets.ViewSet):
    serializer_class = FieldSerializer
    queryset=Field.objects.all()
    def list(self, request, procedure_pk=None, section_pk=None):
        queryset = Field.objects.filter(section__procedure=procedure_pk,section=section_pk)
        serializer = FieldSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, procedure_pk=None, section_pk=None):
        queryset = Field.objects.filter(pk=pk, section=section_pk, section__procedure=procedure_pk)
        field = get_object_or_404(queryset, pk=pk)
        serializer = FieldSerializer(field)
        return Response(serializer.data)
    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if(not serializer.is_valid()):
            return Response({"status":"fail","message":serializer.errors})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success"})
    
class SectionViewSet(viewsets.ViewSet):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    def list(self, request, procedure_pk=None):
        queryset = Section.objects.filter(procedure=procedure_pk)
        serializer = SectionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, procedure_pk=None):
        queryset = Section.objects.filter(pk=pk,procedure=procedure_pk)
        section = get_object_or_404(queryset, pk=pk)
        serializer = SectionSerializer(section)
        return Response(serializer.data)
    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success"})
class ProcedureViewSet(viewsets.ViewSet):
    serializer_class = ProcedureSerializer
    queryset=Procedure.objects.all()
    def list(self, request,):
        queryset = Procedure.objects.all()
        serializer = ProcedureSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Procedure.objects.filter(pk=pk)
        procedure = get_object_or_404(queryset, pk=pk)
        serializer = ProcedureSerializer(procedure)
        return Response(serializer.data)
    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status":"success"})
