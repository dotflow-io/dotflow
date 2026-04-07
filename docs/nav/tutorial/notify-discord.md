# Notify Discord

`NotifyDiscord` sends task notifications to a Discord channel via webhook. You can filter notifications by task status — for example, only receive alerts when a task fails.

## Setup

### 1. Create a webhook

1. Open your Discord server
2. Go to channel settings → **Integrations** → **Webhooks**
3. Click **New Webhook** and copy the URL

/// tip
Store your webhook URL in an environment variable or a `.env` file. Never hardcode secrets in your source code.
///

## Example

{* ./docs_src/notify/notify_discord.py hl[7,23:27,29] *}

## Notification types

| `notification_type` | When notified |
|---------------------|---------------|
| `TypeStatus.FAILED` | Only on failure |
| `TypeStatus.COMPLETED` | Only on success |
| `None` (default) | Every task, regardless of status |

## Show result

Set `show_result=True` to include the task result (as JSON) in the notification embed. Disabled by default to keep messages compact — enable it when you need to inspect output without checking logs.

| `show_result` | Behavior |
|---------------|----------|
| `False` (default) | Only status, workflow ID, and task ID |
| `True` | Adds a `Result` field with the task output as JSON |

## Message format

Notifications are sent as Discord embeds with:

- Task status with emoji indicator
- Workflow ID and Task ID
- Task result as JSON (when `show_result=True`)
- Error details (when failed)

## References

- [NotifyDiscord](https://dotflow-io.github.io/dotflow/nav/reference/notify-discord/)
