# Notify Telegram

`NotifyTelegram` sends task notifications to a Telegram chat via the Bot API. You can filter notifications by task status — for example, only receive alerts when a task fails.

## Setup

### 1. Create a bot

1. Open **Telegram** and search for **BotFather**
2. Type `/newbot` and follow the prompts to name your bot

### 2. Get your bot token

1. Type `/token` in the BotFather chat
2. Select your bot from the list
3. Copy the token — you will need it to configure `NotifyTelegram`

### 3. Get your chat ID

1. Send a message to your bot in Telegram
2. Run the following command:

```bash
curl 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates'
```

3. In the response, find `result[0].message.chat.id` — that is your chat ID

/// tip
Store your token and chat ID in environment variables or a `.env` file. Never hardcode secrets in your source code.
///

## Example

{* ./docs_src/notify/notify_telegram.py hl[7,23:28,30] *}

## Notification types

| `notification_type` | When notified |
|---------------------|---------------|
| `TypeStatus.FAILED` | Only on failure |
| `TypeStatus.COMPLETED` | Only on success |
| `None` (default) | Every task, regardless of status |

## Show result

Set `show_result=True` to include the task result (as JSON) in the notification message. Disabled by default to keep messages compact.

| `show_result` | Behavior |
|---------------|----------|
| `False` (default) | Only status, workflow ID, and task ID |
| `True` | Adds the task output as a JSON code block |

## Message format

Notifications are sent as Telegram messages with:

- Task status with emoji indicator
- Workflow ID and Task ID
- Task result as JSON (when `show_result=True`)
- Error details (when failed)

## References

- [NotifyTelegram](https://dotflow-io.github.io/dotflow/nav/reference/notify-telegram/)
