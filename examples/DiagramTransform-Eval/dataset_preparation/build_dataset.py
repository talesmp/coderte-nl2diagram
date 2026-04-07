"""
Step 0e: Build experiment Excel files from PlantUML data.

Creates Excel datasets for each transformation direction:
- NL2ClassDiagram.xlsx
- NL2UseCaseDiagram.xlsx
- ClassDiagram2NL.xlsx
- UseCaseDiagram2NL.xlsx
"""
import json
import os
import pandas as pd

PLANTUML_DATA_FILE = os.path.join(os.path.dirname(__file__), 'plantuml_data.json')
DATASET_DIR = os.path.join(os.path.dirname(__file__), '..', 'dataset')


def build_nl2classdiagram(data: dict) -> pd.DataFrame:
    """Build NL-to-Class-Diagram dataset."""
    rows = []
    for us_id in sorted(data.keys(), key=lambda x: int(x.replace('US', ''))):
        us = data[us_id]
        rows.append({
            'US_ID': us_id,
            'NL_Description': us['user_story_text'],
            'Target_PlantUML': us['class_diagram_plantuml'],
            'Notation_Type': 'plantuml_class',
        })
    return pd.DataFrame(rows)


def build_nl2usecasediagram(data: dict) -> pd.DataFrame:
    """Build NL-to-Use-Case-Diagram dataset."""
    rows = []
    for us_id in sorted(data.keys(), key=lambda x: int(x.replace('US', ''))):
        us = data[us_id]
        rows.append({
            'US_ID': us_id,
            'NL_Description': us['user_story_text'],
            'Target_PlantUML': us['use_case_diagram_plantuml'],
            'Notation_Type': 'plantuml_usecase',
        })
    return pd.DataFrame(rows)


def build_classdiagram2nl(data: dict) -> pd.DataFrame:
    """Build Class-Diagram-to-NL dataset."""
    rows = []
    for us_id in sorted(data.keys(), key=lambda x: int(x.replace('US', ''))):
        us = data[us_id]
        rows.append({
            'US_ID': us_id,
            'Diagram_PlantUML': us['class_diagram_plantuml'],
            'Target_NL': us['user_story_text'],
            'Notation_Type': 'plantuml_class',
        })
    return pd.DataFrame(rows)


def build_usecasediagram2nl(data: dict) -> pd.DataFrame:
    """Build Use-Case-Diagram-to-NL dataset."""
    rows = []
    for us_id in sorted(data.keys(), key=lambda x: int(x.replace('US', ''))):
        us = data[us_id]
        rows.append({
            'US_ID': us_id,
            'Diagram_PlantUML': us['use_case_diagram_plantuml'],
            'Target_NL': us['user_story_text'],
            'Notation_Type': 'plantuml_usecase',
        })
    return pd.DataFrame(rows)


if __name__ == '__main__':
    with open(PLANTUML_DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Build all 4 datasets
    datasets = {
        'NL2ClassDiagram': build_nl2classdiagram(data),
        'NL2UseCaseDiagram': build_nl2usecasediagram(data),
        'ClassDiagram2NL': build_classdiagram2nl(data),
        'UseCaseDiagram2NL': build_usecasediagram2nl(data),
    }

    for name, df in datasets.items():
        output_dir = os.path.join(DATASET_DIR, name, 'final')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{name}.xlsx')
        df.to_excel(output_path, index=False)
        print(f"{name}: {len(df)} rows -> {output_path}")
