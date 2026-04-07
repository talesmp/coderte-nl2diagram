"""
Step 0a: Parse Diagrams.json from UML-33-UserStory-UseCase-DomainModel.
Extracts structured class diagram and use case diagram data for all 33 US entries.
"""
import json
import os

# Path to the UML-33 dataset repo (sibling of coderte-nl2diagram under githubPersonal)
UML33_REPO = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '..',
    'UML-33-UserStory-UseCase-DomainModel'
))
DIAGRAMS_JSON = os.path.join(UML33_REPO, 'Manually generated UML diagrams', 'Diagrams.json')
US_MAPPING_FILE = os.path.join(os.path.dirname(__file__), 'us_mapping.json')


def normalize_relationship_type(rel_type: str) -> str:
    """Normalize relationship type variants to canonical short form.

    DC types: ASOC, HER, AGR, COMP, DEP
    UC types: E, I
    """
    mapping = {
        'ASOC': 'ASOC',
        'ASOC-Asociacion': 'ASOC',
        'HER': 'HER',
        'HER-Herencia': 'HER',
        'AGR': 'AGR',
        'AGR-Agregacion': 'AGR',
        'COMP': 'COMP',
        'COMP-Composicion': 'COMP',
        'DEP': 'DEP',
        'DEP-Dependencia': 'DEP',
        'E': 'E',
        'I': 'I',
    }
    return mapping.get(rel_type, rel_type)


def parse_class_diagram(dc_data: dict) -> dict:
    """Parse a DC (Domain/Class) section into structured data.

    Returns:
        {
            'classes': {
                'ClassName': {
                    'attributes': [...],
                    'methods': [...]
                }, ...
            },
            'relationships': [
                {'from': str, 'to': str, 'type': str}, ...
            ]
        }
    """
    classes = {}
    for class_name, class_info in dc_data.get('Clases', {}).items():
        classes[class_name] = {
            'attributes': class_info.get('Atributos', []),
            'methods': class_info.get('Metodos', []),
        }

    relationships = []
    for rel in dc_data.get('Relaciones', []):
        if len(rel) >= 3:
            relationships.append({
                'from': rel[0],
                'to': rel[1],
                'type': normalize_relationship_type(rel[2]),
            })

    return {'classes': classes, 'relationships': relationships}


def parse_use_case_diagram(uc_data: dict) -> dict:
    """Parse a UC (Use Case) section into structured data.

    Returns:
        {
            'actors': {
                'ActorName': {
                    'use_cases': [
                        {'id': str, 'type': str, 'name': str}, ...
                    ],
                    'relationships': [
                        {'from_id': str, 'to_id': str, 'type': str}, ...
                    ]
                }, ...
            }
        }
    """
    actors = {}
    for actor_name, actor_data in uc_data.items():
        use_cases = []
        for caso in actor_data.get('Casos', []):
            if len(caso) >= 3:
                use_cases.append({
                    'id': caso[0],
                    'type': caso[1],  # 'CU' = use case, 'A' = actor reference
                    'name': caso[2],
                })

        relationships = []
        for rel in actor_data.get('Relaciones', []):
            if len(rel) >= 3:
                relationships.append({
                    'from_id': rel[0],
                    'to_id': rel[1],
                    'type': normalize_relationship_type(rel[2]),
                })

        actors[actor_name] = {
            'use_cases': use_cases,
            'relationships': relationships,
        }

    return {'actors': actors}


def load_user_story_text(us_id: str, us_mapping: dict) -> str:
    """Load the original English user story text for a given US ID."""
    if us_id not in us_mapping:
        raise ValueError(f"Unknown US ID: {us_id}")

    file_path = os.path.join(UML33_REPO, us_mapping[us_id]['path'])
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"User story file not found: {file_path}")

    # Try utf-8 first, fall back to latin-1 for Windows-encoded files
    for encoding in ['utf-8', 'latin-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read().strip()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Could not decode {file_path} with any supported encoding")


def parse_all() -> dict:
    """Parse Diagrams.json and return structured data for all 33 US entries.

    Returns:
        {
            'US1': {
                'class_diagram': {...},
                'use_case_diagram': {...},
                'user_story_text': str,
            }, ...
        }
    """
    with open(DIAGRAMS_JSON, 'r', encoding='utf-8') as f:
        diagrams = json.load(f)

    with open(US_MAPPING_FILE, 'r', encoding='utf-8') as f:
        us_mapping = json.load(f)

    result = {}
    for us_id in sorted(diagrams.keys(), key=lambda x: int(x.replace('US', ''))):
        us_data = diagrams[us_id]
        cd = parse_class_diagram(us_data.get('DC', {}))
        uc = parse_use_case_diagram(us_data.get('UC', {}))

        try:
            user_story_text = load_user_story_text(us_id, us_mapping)
        except (FileNotFoundError, ValueError, UnicodeDecodeError) as e:
            print(f"Warning: {e}")
            user_story_text = ""

        result[us_id] = {
            'class_diagram': cd,
            'use_case_diagram': uc,
            'user_story_text': user_story_text,
        }

    return result


def print_summary(data: dict):
    """Print a summary of parsed data for verification."""
    for us_id, us_data in sorted(data.items(), key=lambda x: int(x[0].replace('US', ''))):
        cd = us_data['class_diagram']
        uc = us_data['use_case_diagram']
        n_classes = len(cd['classes'])
        n_cd_rels = len(cd['relationships'])
        n_actors = len(uc['actors'])
        n_use_cases = sum(len(a['use_cases']) for a in uc['actors'].values())
        n_us_lines = len(us_data['user_story_text'].splitlines()) if us_data['user_story_text'] else 0
        print(f"{us_id}: {n_classes} classes, {n_cd_rels} CD rels, "
              f"{n_actors} actors, {n_use_cases} UCs, {n_us_lines} US lines")


if __name__ == '__main__':
    data = parse_all()
    print_summary(data)

    # Save parsed data for next steps
    output_path = os.path.join(os.path.dirname(__file__), 'parsed_data.json')
    # Convert to JSON-serializable format
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nParsed data saved to {output_path}")
