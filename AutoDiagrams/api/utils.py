import yaml
from graphviz import Digraph
import os
from .models import Diagram
from django.core.files.base import ContentFile


def get_EA_diagram(yaml_file):
    # Load YAML data
    yaml_data = yaml.safe_load(yaml_file)

    # Initialize Graphviz Digraph object
    dot = Digraph(format='png')
    dot.attr(rankdir='BT')

    # Process YAML data and add nodes and edges to the diagram
    classes = get_classes(yaml_data)
    attributes = []
    for class_name in classes:
        attributes.append(get_attributes(yaml_data, class_name))

    class_attributes = dict(zip(classes, attributes))
    for class_name, class_attrs in class_attributes.items():
        dot.node(class_name)
        for attribute in class_attrs:
            dot.node(attribute)
            dot.edge(class_name, attribute)

    # Save the diagram to a temporary location
    output_path = 'output/er_diagram'
    dot.render(output_path)

    # Read the generated image
    output_image_path = output_path + '.png'
    with open(output_image_path, 'rb') as f:
        image_data = f.read()

    # Save the image to the database
    diagram_content = yaml_file.name.split('.')[0]
    diagram = Diagram(content=diagram_content)
    diagram.file.save(yaml_file.name, yaml_file)
    diagram.image.save(f'{diagram_content}.png', ContentFile(image_data))
    diagram.save()

    if os.path.exists(output_image_path):
        os.remove(output_image_path)

    return diagram
    

def get_classes(yaml_data):
    # Get class names from the YAML data
    classes = []
    for class_name, class_data in yaml_data.items():
        if class_name == 'tags':
            for tag in class_data:
                classes.append(tag.get('name'))
    return classes

def get_attributes(yaml_data, class_name):

    # Get attributes of a class from the YAML data
    attributes = set()
    for path, methods in yaml_data.get('paths', {}).items():
        if path.lstrip('/').split('/')[0] == class_name:
            for details in methods.values():
                if 'parameters' in details:
                    for param in details['parameters']:
                        attributes.add(param['name'])
                if 'requestBody' in details and 'content' in details['requestBody']:
                    for content in details['requestBody']['content'].values():
                        properties = content.get('schema', {}).get('properties', {})
                        for prop_name in properties.keys():
                            attributes.add(prop_name)
    attributes = list(attributes)
    return attributes
