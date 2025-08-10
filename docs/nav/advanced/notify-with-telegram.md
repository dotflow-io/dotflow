# Notify with Telegram

## Bot Telegram

### Create a bot on Telegram:

1 - Open the **Telegram** app on your mobile device.

2 - Tap the **search** icon and look for **BotFather**.

3 - Open the contact and type `/newbot`.

4 - Enter a name for your bot.

### Generate Bot Token:

1 - Type the command `/token`.

2 - Select the bot you just created from the list.

3 - **BotFather** will return an access token — copy and save this token securely. It will be required to authenticate your bot.

### Retrieving Your Telegram Chat ID

1 - Send a message to your bot in Telegram to ensure it appears in the bot's update log.

2 - Run the following `curl` command to fetch the latest updates from your bot:

```bash
curl --location --globoff 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates'
```
> Replace `<YOUR_BOT_TOKEN>` with the token provided by BotFather.

3 - Inspect the API response, and locate the following key `result[0].channel_post.chat.id`. This is your chat ID.

4 - Copy and store the chat ID in a secure location. You will need it to configure the `NotifyTelegram` instance.


## DotFlow Config

### Import

Start with the basics, which is importing the necessary classes and methods.

```python
import os

from dotflow import Config, DotFlow, action
from dotflow.notify import NotifyTelegram
from dotflow.types import TypeStatus
```

### Task function

Use the `@action` decorator to define a simple task that will be executed in the workflow:

```python
@action
def simple_task():
    return "ok"
```


### Notify Class

Instantiate the `NotifyTelegram` class with your Telegram bot credentials. You can use environment variables for security:

```python
notify = NotifyTelegram(
    token=os.getenv("TOKEN"),
    chat_id=os.getenv("CHAT_ID"),
    notification_type=TypeStatus.FAILED  # Notify only on failure
)
```

### Dotflow Class

Pass the `notify` instance into the `Config` class and initialize the `DotFlow` workflow:

```python
workflow = DotFlow(
    config=Config(notify=notify)
)
```

### Add Task

Add your defined task as a step in the workflow:

```python
workflow.task.add(step=simple_task)
```

### Start

Start the workflow execution:

```python
workflow.start()
```
