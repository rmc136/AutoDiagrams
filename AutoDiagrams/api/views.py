from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import YAMLUploadSerializer, GenerateDiagramSerializer, DiagramSerializer
from .models import Diagram
import yaml
import graphviz
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import YAMLUploadForm
from .utils import get_EA_diagram

class UploadYAMLView(APIView):
    def post(self, request):
        serializer = YAMLUploadSerializer(data=request.data)
        if serializer.is_valid():
            yaml_file = request.FILES['yaml_file']
            yaml_content = yaml.safe_load(yaml_file)
            diagram = self.generate_diagram_from_yaml(yaml_content)
            diagram_instance = Diagram.objects.create(content=diagram)
            return Response(DiagramSerializer(diagram_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_diagram_from_yaml(self, yaml_content):
        dot = graphviz.Digraph()
        for key, value in yaml_content.items():
            dot.node(key, value)
        return dot.pipe(format='svg').decode('utf-8')

class GenerateDiagramView(APIView):
    def post(self, request):
        serializer = GenerateDiagramSerializer(data=request.data)
        if serializer.is_valid():
            yaml_content = yaml.safe_load(serializer.validated_data['yaml_content'])
            diagram = self.generate_diagram_from_yaml(yaml_content)
            diagram_instance = Diagram.objects.create(content=diagram)
            return Response(DiagramSerializer(diagram_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_diagram_from_yaml(self, yaml_content):
        dot = graphviz.Digraph()
        for key, value in yaml_content.items():
            dot.node(key, value)
        return dot.pipe(format='svg').decode('utf-8')

class RetrieveDiagramView(APIView):
    def get(self, request, diagram_id):
        try:
            diagram = Diagram.objects.get(id=diagram_id)
            return Response(DiagramSerializer(diagram).data)
        except Diagram.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ListDiagramsView(APIView):
    def get(self, request):
        diagrams = Diagram.objects.all()
        return Response(DiagramSerializer(diagrams, many=True).data)

class DeleteDiagramView(APIView):
    def delete(self, request, diagram_id):
        try:
            diagram = Diagram.objects.get(id=diagram_id)
            diagram.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Diagram.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
def usage_toturial(request):
    return render(request, 'usage_tutorial.html')

def upload_yaml_view(request):
    if request.method == 'POST':
        form = YAMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            yaml_file = request.FILES['yaml_file']
            # Check if the file extension is .yaml or .yml
            if not yaml_file.name.endswith(('.yaml', '.yml')):
                form.add_error('yaml_file', 'File must be in YAML format (.yaml or .yml)')
            else:
                # Generate class diagram and save it to the database with the yaml file content
                diagram = get_EA_diagram(yaml_file)
                
                # Redirect to the success view with the diagram ID
                return HttpResponseRedirect(reverse('upload_success', args=[diagram.id]))
    else:
        form = YAMLUploadForm()
    
    return render(request, 'upload_yaml.html', {'form': form})

def upload_success_view(request, diagram_id):
    # Fetch the diagram from the database using the ID
    diagram = Diagram.objects.get(id=diagram_id)
    yaml_content = diagram.file
    return render(request, 'upload_success.html', {'diagram_path': diagram.image.url, 'yaml_content': yaml_content, 'diagram_id': diagram_id})

def regenerate_diagram_view(request, diagram_id):
    # Fetch the diagram from the database using the ID
    diagram = Diagram.objects.get(id=diagram_id)

    # Read YAML file content
    yaml_content = diagram.file.read()

    # Delete old diagram
    diagram.delete()

    # Generate new diagram
    regenerated_diagram = get_EA_diagram(yaml_content)

    return HttpResponseRedirect(reverse('upload_success', args=[regenerated_diagram.id]))