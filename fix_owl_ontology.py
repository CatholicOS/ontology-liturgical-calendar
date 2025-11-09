#!/usr/bin/env python3
"""
Add proper owl:Ontology declaration to the generated RDF/XML file
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def fix_owl_ontology(input_file, output_file):
    """
    Parse RDF/XML and add owl:Ontology declaration if missing.
    """
    # Define namespaces
    namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
        'owl': 'http://www.w3.org/2002/07/owl#',
        'skos': 'http://www.w3.org/2004/02/skos/core#'
    }

    # Register namespaces
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)

    # Parse the file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Check if owl:Ontology already exists
    ontology_exists = False
    for child in root:
        if child.tag == f"{{{namespaces['rdf']}}}Description" or child.tag == f"{{{namespaces['owl']}}}Ontology":
            about = child.get(f"{{{namespaces['rdf']}}}about")
            if about == "https://example.org/LitCal":
                # Check if it's declared as owl:Ontology
                for type_elem in child.findall(f"{{{namespaces['rdf']}}}type"):
                    resource = type_elem.get(f"{{{namespaces['rdf']}}}resource")
                    if resource == f"{namespaces['owl']}Ontology":
                        ontology_exists = True
                        break

    if not ontology_exists:
        # Create owl:Ontology element
        ontology_elem = ET.Element(f"{{{namespaces['owl']}}}Ontology")
        ontology_elem.set(f"{{{namespaces['rdf']}}}about", "https://example.org/LitCal")

        # Add label
        label = ET.SubElement(ontology_elem, f"{{{namespaces['rdfs']}}}label")
        label.text = "Liturgical Calendar Ontology"

        # Add comment
        comment = ET.SubElement(ontology_elem, f"{{{namespaces['rdfs']}}}comment")
        comment.text = "An ontology for representing liturgical calendar data including events, readings, and calendar settings."

        # Insert at the beginning (after any namespace declarations)
        root.insert(0, ontology_elem)
        print("✓ Added owl:Ontology declaration")
    else:
        print("✓ owl:Ontology declaration already exists")

    # Write the corrected file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"✓ Wrote corrected ontology to: {output_file}")

if __name__ == "__main__":
    base_dir = Path(__file__).parent / "jsondata" / "schemas"

    input_file = base_dir / "LitCal.rdf.xml"
    output_file = base_dir / "LitCal_fixed.owl"

    fix_owl_ontology(input_file, output_file)

    # Also create a prettier version
    print("\nFormatting XML...")
    import subprocess
    result = subprocess.run(
        ["xmllint", "--format", str(output_file)],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        print("✓ Formatted XML with xmllint")
    else:
        print("⚠ xmllint not available, file not formatted")
