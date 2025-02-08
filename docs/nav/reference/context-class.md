# Context class

Here's the reference information for the `Context` class, with all its parameters, attributes and functions.

## Import

You can import the Context class directly from dotflow:

```python
from dotflow import Context
```

## Exemple

`class` dotflow.Context

```python
Context(
    storage={"data": [0, 1, 2, 3]}
)
```

## Parameters

| PARAMETER  | DESCRIPTION      |
|:-----------:|:---------------|
| *`storage` | Attribute where any type of Python object can be stored. <br> **TYPE**: [Any](https://docs.python.org/3/library/typing.html#typing.Any) **DEFAULT**: None|
| `datetime` | Attribute available only for access; sending this parameter is not allowed. It will be assigned a value at runtime with the current date and time. <br> **TYPE**: [datetime](https://docs.python.org/3/library/datetime.html) **DEFAULT**: [datetime.now](https://docs.python.org/3/library/datetime.html#datetime.datetime.now)|