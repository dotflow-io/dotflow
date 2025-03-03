# Welcome to dotflow

![](https://raw.githubusercontent.com/FernandoCelmer/dotflow/master/docs/assets/dotflow.gif)

![GitHub Org's stars](https://img.shields.io/github/stars/dotflow-io?label=Dotflow&style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/dotflow-io/dotflow?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/dotflow?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dotflow?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dotflow?style=flat-square)

This is a very simple library that is still in the early stages of development. The main goal of this tool is to create a simple and secure workflow for executing any type of task. The library's API design was made to make it easy to add tasks and control their execution. To keep it simple, just instantiate the `DotFlow` class, use the `add` method, and the `start` method to begin execution.

Start with the basics [here](https://dotflow-io.github.io/dotflow/nav/getting-started/).

## Getting Help

We use GitHub issues for tracking bugs and feature requests and have limited bandwidth to address them. If you need anything, I ask you to please follow our templates for opening issues or discussions.

- 🐛 [Bug Report](https://github.com/dotflow-io/dotflow/issues/new/choose)
- 📕 [Documentation Issue](https://github.com/dotflow-io/dotflow/issues/new/choose)
- 🚀 [Feature Request](https://github.com/dotflow-io/dotflow/issues/new/choose)
- 💬 [General Question](https://github.com/dotflow-io/dotflow/issues/new/choose)

## Getting Started

### Install

To install `Dotflow`, run the following command from the command line:

**With Pip**

```bash
pip install dotflow
```

**With Poetry**

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

#### 1 - Import

Start with the basics, which is importing the necessary classes and methods. ([DotFlow](https://dotflow-io.github.io/dotflow/nav/reference/dotflow-class/), [action](https://dotflow-io.github.io/dotflow/nav/reference/action-decorator/))

```python
from dotflow import DotFlow, action
```

#### 2 - Callback function

Create a `my_callback` function to receive execution information of a task. `It is not necessary` to include this function, as you will still have a report at the end of the execution in the instantiated object of the `DotFlow` class. This `my_callback` function is only needed if you need to do something after the execution of the task, for example: sending a message to someone, making a phone call, or sending a letter.

```python
def my_callback(*args, **kwargs):
    print(args, kwargs)
```

#### 3 - Task function

Now, create the function responsible for executing your task. It's very simple; just use the [action](https://dotflow-io.github.io/dotflow/nav/reference/action-decorator/) decorator above the function, and that's it—you've created a task. If necessary, you can also add the parameter called `retry` to set the maximum number of execution attempts if the function fails.

```python
@action(retry=5)
def my_task():
    print("task")
```

#### 4 - DotFlow Class

Instantiate the DotFlow class in a `workflow` variable to be used in the following steps. [More details](https://dotflow-io.github.io/dotflow/nav/reference/dotflow-class/).

```python
workflow = DotFlow()
```

#### 5 - Add Task

Now, simply add the `my_task` and `my_callback` functions you created earlier to the workflow using the code below. This process is necessary to define which tasks will be executed and the order in which they will run. The execution order follows the sequence in which they were added to the workflow.

```python
workflow.task.add(step=my_task, callback=my_callback)
```

#### 6 - Start

Finally, just execute the workflow with the following code snippet.

```python
workflow.start()
```

## More Examples

|  | Example                                                                                |
|--| -------------------------------------------------------------------------------------- |
|01| [simple_class_workflow](examples/simple_class_workflow.py)                             |
|02| [simple_function_workflow_with_error](examples/simple_function_workflow_with_error.py) |
|03| [simple_function_workflow](examples/simple_function_workflow.py)                       |
|04| [step_class_result_context](examples/step_class_result_context.py)                     |
|05| [step_class_result_storage](examples/step_class_result_storage.py)                     |
|06| [step_class_result_task](examples/step_class_result_task.py)                           |
|07| [step_function_result_context](examples/step_function_result_context.py)               |
|08| [step_function_result_storage](examples/step_function_result_storage.py)               |
|09| [step_function_result_task](examples/step_function_result_task.py)                     |
|10| [step_with_initial_context](examples/step_with_initial_context.py)                     |
|11| [step_with_many_contexts](examples/step_with_many_contexts.py)                         |
|12| [step_with_previous_context](examples/step_with_previous_context.py)                   |
|13| [workflow_keep_going_true](examples/workflow_keep_going_true.py)                       |
|14| [workflow_step_callback](examples/workflow_step_callback.py)                           |
|15| [workflow_with_callback_failure](examples/workflow_with_callback_failure.py)           |
|16| [workflow_with_callback_success](examples/workflow_with_callback_success.py)           |
|17| [workflow_with_retry](examples/workflow_with_retry.py)                                 |

## Commit Style

- ⚙️ FEATURE
- 📝 PEP8
- 📌 ISSUE
- 🪲 BUG
- 📘 DOCS
- 📦 PyPI
- ❤️️ TEST
- ⬆️ CI/CD
- ⚠️ SECURITY

## License
![GitHub License](https://img.shields.io/github/license/FernandoCelmer/dotflow)

This project is licensed under the terms of the MIT License.
