from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from procedure_app.models import Procedure,Section,Field
from procedure_app.api.serializers import ProcedureSerializer,SectionSerializer,FieldSerializer
from procedure_app.api.paginations import ProcedurePagination
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
                raise ValidationError("Procedure not exists")
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
                raise ValidationError("Give a valid procedure id")
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
    def get_queryset(self):
        section=self.request.query_params.get('section')
        query_set=Field.objects.filter(section=section)
        if not(query_set.exists()):
            raise ValidationError("Give a valid section ID")
        else:
            return query_set

