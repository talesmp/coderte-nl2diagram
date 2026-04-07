"""
Step 0c: Convert translated structured data to PlantUML notation.

Generates PlantUML class diagrams and use case diagrams for all 33 US entries.
"""
import json
import os

TRANSLATED_DATA_FILE = os.path.join(os.path.dirname(__file__), 'translated_data.json')
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), 'plantuml_data.json')

# Mapping from relationship type codes to PlantUML notation
CD_RELATIONSHIP_MAP = {
    'ASOC': '--',       # Association
    'HER': '<|--',      # Inheritance (parent <|-- child)
    'AGR': 'o--',       # Aggregation
    'COMP': '*--',      # Composition
    'DEP': '..>',       # Dependency
}

UC_RELATIONSHIP_MAP = {
    'E': ('..>', '<<extend>>'),    # Extension
    'I': ('..>', '<<include>>'),   # Inclusion
}


def sanitize_plantuml_id(name: str) -> str:
    """Sanitize a name for use as a PlantUML identifier.

    Replaces spaces and special characters with underscores.
    """
    # Replace spaces and hyphens with underscores
    sanitized = name.replace(' ', '_').replace('-', '_').replace('.', '_')
    # Remove any remaining non-alphanumeric characters (except underscore)
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c == '_')
    return sanitized


def generate_class_diagram_plantuml(cd: dict, us_id: str) -> str:
    """Generate PlantUML class diagram notation from structured data.

    Args:
        cd: Class diagram dict with 'classes' and 'relationships'
        us_id: User story identifier for the title

    Returns:
        PlantUML string
    """
    lines = ['@startuml', '']

    # Skip if no classes (some US entries have empty DC sections)
    if not cd['classes']:
        lines.append(f'note "No class diagram data available\\nin Diagrams.json for {us_id}.\\nRequires manual construction." as N')
        lines.append('')
        lines.append('@enduml')
        return '\n'.join(lines)

    # Generate class definitions
    for class_name, class_info in cd['classes'].items():
        safe_name = sanitize_plantuml_id(class_name)
        lines.append(f'class {safe_name} {{')

        for attr in class_info['attributes']:
            if attr:
                lines.append(f'  +{attr}')

        for method in class_info['methods']:
            if method:
                lines.append(f'  +{method}()')

        lines.append('}')
        lines.append('')

    # Generate relationships
    for rel in cd['relationships']:
        from_name = sanitize_plantuml_id(rel['from'])
        to_name = sanitize_plantuml_id(rel['to'])
        rel_type = rel['type']

        if rel_type == 'HER':
            # Inheritance: parent <|-- child (from is parent, to is child)
            arrow = CD_RELATIONSHIP_MAP.get(rel_type, '--')
            lines.append(f'{from_name} {arrow} {to_name}')
        else:
            arrow = CD_RELATIONSHIP_MAP.get(rel_type, '--')
            lines.append(f'{from_name} {arrow} {to_name}')

    lines.append('')
    lines.append('@enduml')
    return '\n'.join(lines)


def generate_use_case_diagram_plantuml(uc: dict, us_id: str) -> str:
    """Generate PlantUML use case diagram notation from structured data.

    Args:
        uc: Use case diagram dict with 'actors'
        us_id: User story identifier for the title

    Returns:
        PlantUML string
    """
    lines = ['@startuml', '']

    if not uc['actors']:
        lines.append(f"' {us_id}: No use case diagram data available")
        lines.append('')
        lines.append('@enduml')
        return '\n'.join(lines)

    # Declare all actors
    for actor_name in uc['actors']:
        safe_actor = sanitize_plantuml_id(actor_name)
        lines.append(f'actor "{actor_name}" as {safe_actor}')
    lines.append('')

    # System boundary rectangle
    lines.append('rectangle "System" {')

    # Declare all use cases inside the system boundary
    # Track use case IDs globally for relationship resolution
    uc_id_map = {}  # (actor_safe_name, uc_id) -> plantuml_alias

    for actor_name, actor_data in uc['actors'].items():
        safe_actor = sanitize_plantuml_id(actor_name)
        for uc_entry in actor_data['use_cases']:
            if uc_entry['type'] == 'CU':
                uc_alias = f"UC_{safe_actor}_{sanitize_plantuml_id(uc_entry['id'])}"
                uc_id_map[(actor_name, uc_entry['id'])] = uc_alias
                uc_label = uc_entry['name']
                lines.append(f'  usecase "{uc_label}" as {uc_alias}')

    lines.append('}')
    lines.append('')

    # Generate actor-to-use-case connections
    for actor_name, actor_data in uc['actors'].items():
        safe_actor = sanitize_plantuml_id(actor_name)
        for uc_entry in actor_data['use_cases']:
            if uc_entry['type'] == 'CU':
                uc_alias = uc_id_map.get((actor_name, uc_entry['id']))
                if uc_alias:
                    # Only connect top-level use cases (no '.' in ID) directly to actor
                    if '.' not in uc_entry['id']:
                        lines.append(f'{safe_actor} --> {uc_alias}')

    lines.append('')

    # Generate use case relationships (extend/include)
    for actor_name, actor_data in uc['actors'].items():
        for rel in actor_data['relationships']:
            from_alias = uc_id_map.get((actor_name, rel['from_id']))
            to_alias = uc_id_map.get((actor_name, rel['to_id']))
            if from_alias and to_alias:
                rel_type = rel['type']
                if rel_type in UC_RELATIONSHIP_MAP:
                    arrow, stereotype = UC_RELATIONSHIP_MAP[rel_type]
                    lines.append(f'{from_alias} {arrow} {to_alias} : {stereotype}')

    lines.append('')
    lines.append('@enduml')
    return '\n'.join(lines)


def convert_all(translated_data: dict) -> dict:
    """Convert all translated data to PlantUML notation.

    Returns:
        {
            'US1': {
                'class_diagram_plantuml': str,
                'use_case_diagram_plantuml': str,
                'user_story_text': str,
            }, ...
        }
    """
    result = {}
    for us_id, us_data in translated_data.items():
        cd_plantuml = generate_class_diagram_plantuml(us_data['class_diagram'], us_id)
        uc_plantuml = generate_use_case_diagram_plantuml(us_data['use_case_diagram'], us_id)

        result[us_id] = {
            'class_diagram_plantuml': cd_plantuml,
            'use_case_diagram_plantuml': uc_plantuml,
            'user_story_text': us_data['user_story_text'],
        }

    return result


def print_sample(data: dict, us_id: str = 'US1'):
    """Print a sample PlantUML output for verification."""
    if us_id not in data:
        print(f"US ID {us_id} not found")
        return

    us = data[us_id]
    print(f"=== {us_id} Class Diagram (PlantUML) ===")
    print(us['class_diagram_plantuml'])
    print()
    print(f"=== {us_id} Use Case Diagram (PlantUML) ===")
    print(us['use_case_diagram_plantuml'])
    print()
    print(f"=== {us_id} User Stories (first 5 lines) ===")
    for line in us['user_story_text'].splitlines()[:5]:
        print(line)


if __name__ == '__main__':
    with open(TRANSLATED_DATA_FILE, 'r', encoding='utf-8') as f:
        translated_data = json.load(f)

    plantuml_data = convert_all(translated_data)

    # Print samples at different complexity levels
    for sample_id in ['US1', 'US3', 'US23']:
        print_sample(plantuml_data, sample_id)
        print('\n' + '=' * 60 + '\n')

    # Save output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(plantuml_data, f, indent=2, ensure_ascii=False)
    print(f"PlantUML data saved to {OUTPUT_FILE}")
