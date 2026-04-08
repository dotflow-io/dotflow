# Notifications on Failure

Configure your workflow to send notifications only when tasks fail. Useful for monitoring production pipelines without being flooded by success messages.

## Example with Telegram

{* ./docs_src/advanced/notifications_on_failure.py hl[2,25:30,36] *}

## How it works

1. `NotifyTelegram` is configured with `notification_type=TypeStatus.FAILED`
2. After each task status changes, dotflow calls `notify.hook_status_task(task)`
3. The provider checks if `task.status` matches the configured `notification_type`
4. Only failed tasks trigger a Telegram message

## Notification types

| Type | When notified |
|------|---------------|
| `TypeStatus.FAILED` | Only on failure |
| `TypeStatus.COMPLETED` | Only on success |
| `None` (default) | Every task, regardless of status |

## References

- [NotifyTelegram](https://dotflow-io.github.io/dotflow/nav/reference/notify-telegram/)
- [NotifyDiscord](https://dotflow-io.github.io/dotflow/nav/reference/notify-discord/)
- [Notify Provider](https://dotflow-io.github.io/dotflow/nav/tutorial/notify-default/)
- [Error Handling](https://dotflow-io.github.io/dotflow/nav/tutorial/error-handling/)
