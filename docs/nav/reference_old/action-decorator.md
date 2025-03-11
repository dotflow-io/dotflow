# Action decorator

Here's the reference information for the `action` decorator.

### Import

You can import the action decorator directly from dotflow:

```python
from dotflow import action
```

### Examples

#### Standard

`class` dotflow.action

```python
@action
def my_task():
    print("task")
```

#### With Retry

`class` dotflow.action

```python
@action(retry=5)
def my_task():
    print("task")
```

### Parameters

| PARAMETER  | DESCRIPTION      |
|:-----------:|:---------------|
| `retry` | Integer-type parameter referring to the number of retry attempts the function will execute in case of failure. |
