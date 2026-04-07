# CodeRTE: LLM-Based Evaluation of NL-to-Diagram and Diagram-to-NL Transformations

This repository adapts the **CodeRPE** (Code Role-Player Evaluation) framework from [Wu et al., IEEE TSE 2025](Can_Large_Language_Models_Serve_as_Evaluators_for_Code_Summarization.pdf) to evaluate transformations between natural language (user stories) and UML diagrams.

## Overview

CodeRPE demonstrated that LLMs, when assigned expert personas, can effectively evaluate code summaries across multiple quality dimensions. We extend this methodology to four transformation directions involving UML class diagrams and use case diagrams, represented in PlantUML notation.

### Transformation Directions

| Direction | Input | Output |
|---|---|---|
| **NL2ClassDiagram** | User Stories (NL) | Class Diagram (PlantUML) |
| **NL2UseCaseDiagram** | User Stories (NL) | Use Case Diagram (PlantUML) |
| **ClassDiagram2NL** | Class Diagram (PlantUML) | NL Description |
| **UseCaseDiagram2NL** | Use Case Diagram (PlantUML) | NL Description |

### Evaluation Dimensions

For **NL-to-Diagram** directions, LLM evaluators assess:
- **Structural Correctness** -- Valid PlantUML syntax and proper diagram elements
- **Semantic Fidelity** -- Faithful representation of the source requirements
- **Notation Quality** -- Correct UML conventions and naming
- **Completeness** -- All essential elements captured without redundancies

For **Diagram-to-NL** directions:
- **Coherence** -- Well-structured, logically organized description
- **Consistency** -- Factual alignment with the diagram, no hallucinations
- **Fluency** -- Grammatically correct, natural prose
- **Relevance** -- Important elements captured without excess detail

## Dataset

The gold-standard dataset is derived from the [PyUNML dataset](https://github.com/matovaro/PyUNML-DataSet), containing **33 user story sets** paired with manually crafted UML class diagrams and use case diagrams. Original diagram labels were translated from Spanish to English and converted to PlantUML notation.

| Metric | Count |
|---|---|
| User story sets | 33 |
| Actors (across all UC diagrams) | 258 |
| Use cases | 2,014 |
| Classes (across all CD) | 341 |
| Attributes and methods | 2,389 |

## Repository Structure

```
coderte-nl2diagram/
├── examples/
│   ├── CodeSum-Eval/                    # Original CodeRPE experiment (reference)
│   │   ├── RQ1/                         # Role-player evaluation
│   │   ├── RQ2/                         # Ablation study
│   │   ├── RQ3/                         # Full pipeline + BLEU
│   │   └── utils/                       # Correlation metrics
│   │
│   └── DiagramTransform-Eval/           # Our adapted experiment
│       ├── dataset_preparation/         # Parse, translate, convert pipeline
│       ├── dataset/                     # Excel files + human review materials
│       │   ├── human_review/            # 33 x (UserStories.txt + CD.puml + UC.puml + PNGs)
│       │   ├── NL2ClassDiagram/
│       │   ├── NL2UseCaseDiagram/
│       │   ├── ClassDiagram2NL/
│       │   └── UseCaseDiagram2NL/
│       ├── common/                      # Shared API client, config, score extraction
│       ├── NL2ClassDiagram/             # Prompts + RQ1-RQ3 scripts
│       ├── NL2UseCaseDiagram/
│       ├── ClassDiagram2NL/
│       ├── UseCaseDiagram2NL/
│       ├── utils/                       # Correlation, validators, metrics
│       └── experiment_proposal.tex      # LaTeX experiment proposal
│
├── Can_Large_Language_Models_...pdf     # Reference paper (Wu et al., 2025)
├── pyproject.toml                       # Project config and dependencies
├── uv.lock                              # Dependency lockfile (reproducibility)
└── LICENSE
```

## Getting Started

### Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and reproducibility.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies from the lockfile
uv sync
```

To run any script:

```bash
uv run python examples/DiagramTransform-Eval/dataset_preparation/build_dataset.py
```

### Dataset Preparation

The dataset preparation pipeline (already executed, outputs included in repo):

```bash
cd examples/DiagramTransform-Eval/dataset_preparation

# Step 1: Parse Diagrams.json from PyUNML
python parse_diagrams_json.py

# Step 2: Translate Spanish labels to English
python translate_to_english.py

# Step 3: Convert to PlantUML notation
python convert_to_plantuml.py

# Step 4: Build experiment Excel files
python build_dataset.py
```

## Acknowledgments

- **CodeRPE framework**: Wu et al., "Can Large Language Models Serve as Evaluators for Code Summarization?", IEEE TSE 2025. Original code: [CGCL-codes/naturalcc](https://github.com/CGCL-codes/naturalcc)
- **PyUNML dataset**: [matovaro/PyUNML-DataSet](https://github.com/matovaro/PyUNML-DataSet)
- **User story collections**: Dalpiaz et al. (2018, 2020)

## License

[MIT](LICENSE)
