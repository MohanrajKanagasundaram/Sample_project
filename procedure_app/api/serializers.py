from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from procedure_app.models import Procedure,Section,Field

class FieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False)
    class Meta:
        model=Field
        exclude=['section',]
    def validate_type(self,value):
        if(value not in ['singleline', 'checkbox', 'paragraph', 'radio']):
            raise ValidationError('Not valid')
        else:
            return value
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
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        fields = validated_data.get('field')
        if(fields!=None):
            print(fields)
            for field in fields :
                field_id = field.get('id',None)
    
                if field_id:
                    required_field = Field.objects.get(id=field_id, section=instance)
                    required_field.label = field.get('label',required_field.label)
                    required_field.type = field.get('field', required_field.type)
                    required_field.options = field.get('options',required_field.options)
                    required_field.is_table = field.get('is_table', required_field.is_table)
                    required_field.validations = field.get('validations',required_field.validations)
                    required_field.target = field.get('target',required_field.target)
                    required_field.save()
                    
                else:
                    Field.objects.create(section=instance, **field)
        instance.save()
        return instance  
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
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        sections = validated_data.get('section')
        if(sections!=None):
            for section in sections:
                section_id = section.get('id',None)
                if section_id:
                    required_section = Section.objects.get(id=section_id, procedure=instance)
                    required_section.name=section.get('name',required_section.name)
                    required_section.save()
                    
                    
                    
                else:
                    Field.objects.create(procedure=instance, **section)

        return instance