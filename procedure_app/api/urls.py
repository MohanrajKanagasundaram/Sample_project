from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from django.conf.urls import handler404
from procedure_app.api.views import ProcedureView,SectionView,FieldView
from procedure_app.api.views import FieldViewSet,SectionViewSet,ProcedureViewSet,ErrorView
router = DefaultRouter()
router.register(r'procedures', ProcedureViewSet, basename='procedures')

section_router = routers.NestedSimpleRouter(router, r'procedures', lookup='procedure')
section_router.register(r'sections', SectionViewSet, basename='sections')

field_router = routers.NestedSimpleRouter(section_router, r'sections', lookup='section')
field_router.register(r'fields', FieldViewSet, basename='fields')

urlpatterns = [
   path(r'', include(router.urls)),
   path(r'', include(section_router.urls)),
   path(r'', include(field_router.urls)),
   # path('',ProcedureView.as_view(),name='Procedure List'),
   # path('<int:pk>/',ProcedureView.as_view(),name='Procedure'),
   # path('section/',SectionView.as_view(),name='section'),
   # path('section/<int:pk>/',SectionView.as_view(),name='section'),
   # path('section/field/',FieldView.as_view(),name='field'),
   # path('section/field/<int:pk>/',FieldView.as_view(),name='field'),
   # path(r'<str:pk>',ErrorView,name="page not found error")
]

