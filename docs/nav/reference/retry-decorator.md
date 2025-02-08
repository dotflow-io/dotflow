# Retry decorator

## Import

You can import the action decorator directly from dotflow:

```python
from dotflow import retry
```

## Example

`class` dotflow.retry

```python
@action
@retry(max_retry=1)
def my_task():
    print("task")
    raise Exception("Task Error!")
```

## Parameters

| PARAMETER  | DESCRIPTION      |
|:-----------:|:---------------|
| *`max_retry` | Maximum number of retries that the function should be executed if there is an error. <br> **TYPE**: int **DEFAULT**: 1 |