# Start Function

Here's the reference information for the `start` function.

### Example

`class` dotflow.DotFlow.start

```python
workflow.start()
```

### Parameters

| PARAMETER     | DESCRIPTION |
|---------------|-----------------|
| `keep_going`  | A parameter that receives a boolean object with the purpose of continuing or not the execution of the workflow in case of an error during the execution of a task. If it is **true**, the execution will continue; if it is **False**, the workflow will stop. <hr> **TYPE**: [bool](https://docs.python.org/3/library/functions.html#bool) **DEFAULT**: false |
| `mode`        | A parameter for assigning the execution mode of the workflow. Currently, there is the option to execute in **sequential** mode or **background** mode. By default, it is in **sequential** mode. <hr> **TYPE**: [str](https://docs.python.org/3/library/stdtypes.html#str) **DEFAULT**: "sequential" |
