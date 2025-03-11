# Getting Started

February 10, 2025

---

## Install

To install **Dotflow**, run the following command from the command line:

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
from dotflow import DotFlow, action

def my_callback(*args, **kwargs):
    print(args, kwargs)

@action(retry=5)
def my_task():
    print("task")

workflow = DotFlow()
workflow.task.add(step=my_task, callback=my_callback)
workflow.start()
```

### 1 - Import

Start with the basics, which is importing the necessary classes and methods. ([DotFlow](https://dotflow-io.github.io/dotflow/nav/reference/dotflow/), [action](https://dotflow-io.github.io/dotflow/nav/reference/action/))

```python
from dotflow import DotFlow, action
```

### 2 - Callback function

Create a `my_callback` function to receive execution information of a task. `It is not necessary` to include this function, as you will still have a report at the end of the execution in the instantiated object of the `DotFlow` class. This `my_callback` function is only needed if you need to do something after the execution of the task, for example: sending a message to someone, making a phone call, or sending a letter. [More details](https://dotflow-io.github.io/dotflow/nav/reference/utils/#dotflow.utils.basic_functions.basic_callback)

```python
def my_callback(*args, **kwargs):
    print(args, kwargs)
```

### 3 - Task function

Now, create the function responsible for executing your task. It's very simple; just use the [action](https://dotflow-io.github.io/dotflow/nav/reference/action/) decorator above the function, and that's it—you've created a task. If necessary, you can also add the parameter called `retry` to set the maximum number of execution attempts if the function fails. [More details](https://dotflow-io.github.io/dotflow/nav/reference/utils/#dotflow.utils.basic_functions.basic_function)

```python
@action(retry=5)
def my_task():
    print("task")
```

### 4 - DotFlow Class
Instantiate the DotFlow class in a `workflow` variable to be used in the following steps. [More details](https://dotflow-io.github.io/dotflow/nav/reference/dotflow/).

```python
workflow = DotFlow()
```

### 5 - Add Task

Now, simply add the `my_task` and `my_callback` functions you created earlier to the workflow using the code below. This process is necessary to define which tasks will be executed and the order in which they will run. The execution order follows the sequence in which they were added to the workflow. [More details](https://dotflow-io.github.io/dotflow/nav/reference/task-builder/#dotflow.core.task.TaskBuilder.add)

```python
workflow.task.add(step=my_task, callback=my_callback)
```

### 6 - Start

Finally, just execute the workflow with the following code snippet. [More details](https://dotflow-io.github.io/dotflow/nav/reference/workflow/#dotflow.core.workflow.Workflow)

```python
workflow.start()
```
