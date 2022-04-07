from django.urls import path
from procedure_app.api.views import ProcedureView,SectionView,FieldView

urlpatterns = [
   path('',ProcedureView.as_view(),name='Procedure List'),
   path('<int:pk>/',ProcedureView.as_view(),name='Procedure'),
   path('section/',SectionView.as_view(),name='section'),
   path('section/<int:pk>/',SectionView.as_view(),name='section'),
   path('section/field/',FieldView.as_view(),name='field'),
   path('section/field/<int:pk>/',FieldView.as_view(),name='field')
]
