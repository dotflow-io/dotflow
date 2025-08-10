# First Steps

## 1. Import

Start with the basics, which is importing the necessary classes and methods. ([DotFlow](https://dotflow-io.github.io/dotflow/nav/reference/dotflow/), [action](https://dotflow-io.github.io/dotflow/nav/reference/action/))

{* ./docs_src/first_steps/first_steps.py ln[1:1] *}

## 2. Callback function

Create a `my_callback` function to receive execution information of a task. `It is not necessary` to include this function, as you will still have a report at the end of the execution in the instantiated object of the `DotFlow` class. This `my_callback` function is only needed if you need to do something after the execution of the task, for example: sending a message to someone, making a phone call, or sending a letter. [More details](https://dotflow-io.github.io/dotflow/nav/reference/utils/#dotflow.utils.basic_functions.basic_callback)

{* ./docs_src/first_steps/first_steps.py ln[4:5] *}

## 3. Task function

Now, create the function responsible for executing your task. It's very simple; just use the [action](https://dotflow-io.github.io/dotflow/nav/reference/action/) decorator above the function, and that's it—you've created a task.

{* ./docs_src/first_steps/first_steps.py ln[8:10] *}

## 4. DotFlow Class
Instantiate the DotFlow class in a `workflow` variable to be used in the following steps. [More details](https://dotflow-io.github.io/dotflow/nav/reference/dotflow/).

{* ./docs_src/first_steps/first_steps.py ln[13] *}

## 5. Add Task

Now, simply add the `my_task` and `my_callback` functions you created earlier to the workflow using the code below. This process is necessary to define which tasks will be executed and the order in which they will run. The execution order follows the sequence in which they were added to the workflow. [More details](https://dotflow-io.github.io/dotflow/nav/reference/task-builder/#dotflow.core.task.TaskBuilder.add)

{* ./docs_src/first_steps/first_steps.py ln[14] *}

## 6. Start

Finally, just execute the workflow with the following code snippet. [More details](https://dotflow-io.github.io/dotflow/nav/reference/workflow/#dotflow.core.workflow.Manager)

{* ./docs_src/first_steps/first_steps.py ln[15] *}


## Full Code

The simplest file could look like this:

{* ./docs_src/first_steps/first_steps.py *}
