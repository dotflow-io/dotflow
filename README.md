# Welcome to dotflow

![](https://raw.githubusercontent.com/FernandoCelmer/dotflow/master/docs/assets/dotflow.gif)

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
workflow.task.add(step=my_task, callback=callback)
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

This project is licensed under the terms of the GNU General Public License v3.0.