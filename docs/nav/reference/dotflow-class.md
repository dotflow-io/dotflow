# Dotflow class

Here's the reference information for the `DotFlow` class, with all its parameters, attributes and functions.

## Import

You can import the Dotflow class directly from dotflow:

```python
from dotflow import DotFlow
```

## Exemple

`class` dotflow.DotFlow

```python
DotFlow(
    title="My Workflow",
    initial_context={"data": [0, 1, 2, 3]}
)
```

## Parameters

| PARAMETER  | DESCRIPTION      |
|:-----------:|:---------------|
| `title` | Reference title of the workflow. This title is used for documentation purposes and also for differentiation in contexts where many workflows are being executed. <br> **TYPE**: [string](https://docs.python.org/3/library/stdtypes.html#str) **DEFAULT**: ""|
| `initial_context`            | The parameter has the main objective of including initial data in the execution of the workflow. This parameter can be accessed internally to retrieve this information and process it if necessary, according to the logic or objective of the workflow. <br> **TYPE**: [Any](https://docs.python.org/3/library/typing.html#typing.Any) **DEFAULT**: [Context](https://fernandocelmer.github.io/dotflow/nav/reference/context-class/) |

## Functions

### task

`class` dotflow.DotFlow.task

| Function  | Description   |
|-----------|---------------|
| `add`     |               |

### start

`class` dotflow.DotFlow.start

| Function      | Description   |
|---------------|---------------|
| `sequential`  |               |
| `background`  |               |
| `parallel`    |               |
| `data_store`  |               |