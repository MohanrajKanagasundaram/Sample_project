from rest_framework import serializers
from procedure_app.models import Procedure,Section,Field

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model=Field
        exclude=['section',]
        
class SectionSerializer(serializers.ModelSerializer):
    field=FieldSerializer(many=True)
    class Meta:
        model=Section
        exclude=['procedure']
    def create(self, validated_data):
        field_validated_data = validated_data.pop('field')
        section = Section.objects.create(**validated_data)
        for each in field_validated_data:
            Field.objects.create(section=section,**each)
        return section
        
        
class ProcedureSerializer(serializers.ModelSerializer):
    section=SectionSerializer(many=True)
    class Meta:
        model=Procedure
        fields='__all__'
        
    def create(self, validated_data):
        section_validated_data = validated_data.pop('section')
        procedure = Procedure.objects.create(**validated_data)
        section_serializer = self.fields['section']
        for each in section_validated_data:
            each['procedure'] = procedure
        section= section_serializer.create(section_validated_data)
        return procedure