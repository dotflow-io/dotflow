# Notify Provider

The `notify` provider defines how workflow/task notifications are emitted.

## Available providers

- `NotifyDefault`: no external notification channel.
- `NotifyTelegram`: sends notifications to Telegram.

## Example

{* ./docs_src/config/notify_provider.py ln[1:32] hl[13:14,17:23,26] *}

Telegram setup example:

{* ./docs_src/notify/notify_telegram.py ln[1:41] hl[26:30,32:35] *}

## References

- [NotifyDefault](https://dotflow-io.github.io/dotflow/nav/reference/notify-default/)
- [NotifyTelegram](https://dotflow-io.github.io/dotflow/nav/reference/notify-telegram/)
