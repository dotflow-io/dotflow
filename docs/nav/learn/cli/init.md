# Init

Scaffold a new dotflow project interactively.

```bash
dotflow init
```

The command prompts for project configuration:

```
project_name [my-pipeline]: my-etl
storage [default]: s3
```

Output:

```
my-etl/
├── my_etl/
│   ├── __init__.py
│   ├── actions.py
│   └── workflow.py
├── tests/
│   └── test_workflow.py
├── pyproject.toml
└── README.md
```

## Storage options

| Option | Description |
|--------|-------------|
| `default` | In-memory, no persistence |
| `file` | Local disk (StorageFile) |
| `s3` | AWS S3 (StorageS3) — adds `dotflow[aws]` dependency |
| `gcs` | Google Cloud Storage (StorageGCS) — adds `dotflow[gcp]` dependency |

## Running the generated project

```bash
cd my-etl
pip install -e .
python -m my_etl.workflow
```

## Running the generated tests

```bash
pytest
```
