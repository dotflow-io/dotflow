# Getting Started

February 7, 2025

---

## Install

To install Dotflow, run the following command from the command line:

### With Pip

```bash
pip install dotflow
```

###  With Poetry

```bash
poetry add dotflow
```

## First Steps

The simplest file could look like this:

```python
from dotflow import DotFlow, action, retry

def callback(**kwargs):
    print(kwargs)

@action
@retry(max_retry=1)
def my_task():
    print("task")

workflow.task.add(step=my_task, callback=callback)
workflow.start(workflow=workflow).sequential()
``` 