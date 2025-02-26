# Add Function

Here's the reference information for the `add` function.

### Example

`class` dotflow.DotFlow.task.add

```python
workflow.task.add(step=my_task, callback=my_callback)
```

### Parameters

| Function          | DESCRIPTION   |
|-------------------|---------------|
| *`step`            | A parameter that receives an object of the callable type, which is basically a function. You can see in this [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#3-task-function). <hr> **TYPE**: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable) **DEFAULT**: _____|
| `initial_context` | The parameter exists to include initial data in the execution of the workflow within the **function context**. This parameter can be accessed internally, for example: **initial_context**, to retrieve this information and manipulate it if necessary, according to the objective of the workflow. <hr> **TYPE**: [Any](https://docs.python.org/3/library/typing.html#typing.Any) **DEFAULT**: [Context](https://dotflow-io.github.io/dotflow/nav/reference/context-class/)| [Context](https://dotflow-io.github.io/dotflow/nav/reference/context-class/) |
| `callback`        | Any callable object that receives **args** or **kwargs**, which is basically a function. You can see in this [example](https://dotflow-io.github.io/dotflow/nav/getting-started/#2-callback-function). <hr> **TYPE**: [Callable](https://docs.python.org/3/library/typing.html#typing.Callable) **DEFAULT**: _____|
