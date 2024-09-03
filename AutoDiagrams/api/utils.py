import yaml
from graphviz import Digraph
import os
from .models import Diagram
from django.core.files.base import ContentFile


from graphviz import Digraph
import yaml
from django.core.files.base import ContentFile
import os

def get_EA_diagram(yaml_file):
    # Read file content if it's a FileField
    if hasattr(yaml_file, 'read'):
        yaml_file_content = yaml_file.read()
    else:
        yaml_file_content = yaml_file

    # Load YAML data
    yaml_data = yaml.safe_load(yaml_file_content)

    # Initialize Graphviz Digraph object
    dot = Digraph(format='png')
    dot.attr(rankdir='LR', nodesep='0.75', ranksep='0.75')

    # Get classes and their attributes
    classes = get_classes(yaml_data)
    class_attributes = {cls: get_attributes(yaml_data, cls) for cls in classes}

    # Create nodes for each class and its attributes
    for class_name, attrs in class_attributes.items():
        # Add the class node
        dot.node(class_name, shape='rect', style='filled')

        # Add a subgraph (cluster) for the class's attributes
        with dot.subgraph() as s:
            s.attr(rank='same')
            s.attr(label=f'{class_name} Attributes', style='dashed')

            # Add attribute nodes within the subgraph
            for attribute in attrs:
                attribute_node_name = f"{class_name}_{attribute}"
                s.node(attribute_node_name, shape='ellipse')
                # Add edges from class to its attributes
                dot.edge(class_name, attribute_node_name)

    # Save the diagram to a temporary location
    output_path = 'output/er_diagram'
    dot.render(output_path)

    # Read the generated image
    output_image_path = output_path + '.png'
    with open(output_image_path, 'rb') as f:
        image_data = f.read()

    # Create a unique filename for the YAML file and image
    yaml_filename = 'diagram.yaml'  # or another unique name
    image_filename = f'{yaml_filename.split(".")[0]}.png'

    # Save the image to the database
    diagram_content = yaml_file_content.decode('utf-8') if hasattr(yaml_file_content, 'decode') else yaml_file_content
    diagram = Diagram(content=diagram_content)
    diagram.file.save(yaml_filename, ContentFile(yaml_file_content))  # Use ContentFile to save file
    diagram.image.save(image_filename, ContentFile(image_data))
    diagram.save()

    # Clean up the temporary file
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
    return list(attributes)