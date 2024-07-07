import yaml
from graphviz import Digraph

def generate_class_diagram(yaml_file):
    # Load YAML data
    yaml_data = yaml.safe_load(yaml_file)
    
    # Initialize Graphviz Digraph object
    dot = Digraph(format='png')
    print(yaml_data)
    # Process YAML data and add nodes and edges to the diagram
    for class_name, class_data in yaml_data.items():
        # Add class node
        dot.node(class_name, class_name, shape='rectangle')
        
        # Add edges (e.g., for inheritance)
        if 'inherits' in class_data:
            parent_class = class_data['inherits']
            dot.edge(parent_class, class_name)
        
        # Add attributes and methods (if available)
        if 'attributes' in class_data:
            for attribute in class_data['attributes']:
                dot.node(attribute, attribute, shape='ellipse')
                dot.edge(class_name, attribute)
        
        if 'methods' in class_data:
            for method in class_data['methods']:
                dot.node(method, method, shape='ellipse')
                dot.edge(class_name, method)
    
    # Render the diagram to a PNG image
    diagram_path = '/path/to/generated/diagram.png'  # Replace with actual path
    dot.render(diagram_path, view=False)
    
    return diagram_path