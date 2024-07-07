from rest_framework import serializers
from .models import Diagram

class YAMLUploadSerializer(serializers.Serializer):
    yaml_file = serializers.FileField()

class GenerateDiagramSerializer(serializers.Serializer):
    yaml_content = serializers.CharField()

class DiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagram
        fields = '__all__'