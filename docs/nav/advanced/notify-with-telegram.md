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

Use the runnable example below:

{* ./docs_src/notify/notify_telegram.py ln[1:41] hl[26:30,32:35] *}
