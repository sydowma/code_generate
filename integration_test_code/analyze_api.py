import os

from langchain_community.document_loaders import TextLoader
from tree_sitter import Language, Parser
import tree_sitter_java as java

__doc__ = """
use tree-sitter to analyse Java code and find API endpoint

"""

JAVA_LANGUAGE = Language(java.language())

class AnalyzeAPI:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def analyze(self):
        # scan package for all files
        # based on java file
        java_files = []
        # scan package for all files based on java file
        for root, dirs, files in os.walk(self.dir_path):
            for file in files:
                if file.endswith('Controller.java'):
                    java_files.append(os.path.join(root, file))

        print("all controller file = ", java_files)
        # Now java_files contains the paths to all .java files in the directory
        result = []
        for java_file in java_files:
            # You can add your analysis logic here
            print(f"Analyzing file: {java_file}")
            # Example: Load and parse the Java file using tree-sitter
            parser = Parser(JAVA_LANGUAGE)
            with open(java_file, 'r', encoding='utf-8') as f:
                tree = parser.parse(f.read().encode('utf-8'))
                api_information = self.find_api_endpoints(tree.root_node, java_file)
                if len(api_information) > 0:
                    result.extend(api_information)
        print("api_information = ", result)
        print(result)

    def find_api_endpoints(self, node, java_file):
        """
        Finds API endpoints in the given node using iteration.
        """
        result = []
        nodes_to_visit = [node]
        
        while nodes_to_visit:
            current_node = nodes_to_visit.pop(0)
            
            if current_node.type == 'method_declaration':
                annotations = self.get_annotations(current_node)
                for annotation in annotations:
                    if annotation['type'] in ['RequestMapping', 'GetMapping', 'PostMapping', 'PutMapping', 'DeleteMapping']:
                        method_name = self.get_method_name(current_node)
                        result.append({
                            'method': method_name,
                            'type': annotation['type'],
                            'api_path': annotation['path'],
                            'file_path': java_file,
                            # parameters
                            # body
                        })
            
            # Add all children to the queue
            nodes_to_visit.extend(current_node.children)
            
        return result

    def get_annotations(self, node):
        """
        Extracts annotations from a given node.
        """
        annotations = []
        for child in node.children:
            if child.type == 'modifiers':  # Change from 'annotation' to 'modifiers'
                for modifier in child.children:  # Iterate through modifier children
                    annotations_text = modifier.text.decode("utf-8").strip()
                    if annotations_text.startswith('@'):  # Check if it's an annotation
                        mapping_type = None
                        value = None
                        
                        # Extract the mapping type
                        mapping_type = annotations_text.split('@')[1].split('(')[0]
                        
                        # Extract the value if present
                        if '(' in annotations_text and ')' in annotations_text:
                            value = annotations_text.split('(')[1].split(')')[0]
                        else:
                            value = ""
                        
                        if mapping_type in ['RequestMapping', 'GetMapping', 'PostMapping', 'PutMapping', 'DeleteMapping']:
                            annotations.append({'type': mapping_type, 'path': value})
        return annotations

    def get_annotation_value(self, node):
        value_node = node.child_by_field_name('value')
        if value_node:
            return value_node.text.decode('utf-8').strip('"')
        return ""

    def get_method_name(self, node):
        name_node = node.child_by_field_name('name')
        if name_node:
            return name_node.text.decode('utf-8')
        return ""

if __name__ == '__main__':
    api = AnalyzeAPI(dir_path='/Users/oker/github/code_generate')
    api.analyze()
