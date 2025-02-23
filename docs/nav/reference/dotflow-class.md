# Dotflow class

Here's the reference information for the `DotFlow` class, with all its parameters, attributes and functions.

## Import

You can import the Dotflow class directly from dotflow:

```python
from dotflow import DotFlow
```

## Example

`class` dotflow.DotFlow

```python
DotFlow(
    initial_context={"data": [0, 1, 2, 3]}
)
```

## Parameters

| PARAMETER  | DESCRIPTION      |
|:-----------:|:---------------|
| `initial_context`            | The parameter exists to include initial data in the execution of the workflow within the **class context**. This parameter can be accessed internally, for example: **self.initial_context**, to retrieve this information and manipulate it if necessary, according to the objective of the workflow. <hr> **TYPE**: [Any](https://docs.python.org/3/library/typing.html#typing.Any) **DEFAULT**: [Context](https://dotflow-io.github.io/dotflow/nav/reference/context-class/) |

## Functions

### add

`class` dotflow.DotFlow.task.add

| Function          | DESCRIPTION   |
|-------------------|---------------|
| *`step`            | A parameter that receives an object of the callable type, which is basically a function. You can see in this [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function). <hr> **TYPE**: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable) **DEFAULT**: _____|
| `initial_context` | The parameter exists to include initial data in the execution of the workflow within the **function context**. This parameter can be accessed internally, for example: **initial_context**, to retrieve this information and manipulate it if necessary, according to the objective of the workflow. <hr> **TYPE**: [Any](https://docs.python.org/3/library/typing.html#typing.Any) **DEFAULT**: [Context](https://dotflow-io.github.io/dotflow/nav/reference/context-class/)| [Context](https://dotflow-io.github.io/dotflow/nav/reference/context-class/) |
| `callback`        | Any callable object that receives **args** or **kwargs**, which is basically a function. You can see in this [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#2-callback-function). <hr> **TYPE**: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable) **DEFAULT**: _____|

### start

`class` dotflow.DotFlow.start

| PARAMETER     | DESCRIPTION |
|---------------|-----------------|
| `keep_going`  | A parameter that receives a boolean object with the purpose of continuing or not the execution of the workflow in case of an error during the execution of a task. If it is **true**, the execution will continue; if it is **false**, the workflow will stop. <hr> **TYPE**: [bool](https://docs.python.org/3/library/functions.html#bool) **DEFAULT**: false |
| `mode`        | A parameter for assigning the execution mode of the workflow. Currently, there is the option to execute in **sequential** mode or **background** mode. By default, it is in **sequential** mode. <hr> **TYPE**: [str](https://docs.python.org/3/library/stdtypes.html#str) **DEFAULT**: "sequential" |
