# Daesoop Bot

Daesoop Bot is an **anonymous message relay bot** for Discord servers. It allows server members to post messages and media (photos, videos, audio) to a channel without revealing their identity, while providing administrators with secure management tools.

## What does Daesoop Bot do?

- Use the `/bamboo` command to open a private composition window; when you submit text and files, the bot posts them to the designated channel **without revealing the author's information**.
- Posted messages include buttons accessible only to administrators:
- **View Author** - Only administrators can see the actual author of the message (visible only to the administrator who clicks it). 
- **Manage** - Administrators can issue timeouts to users causing issues or permanently ban them from using Daesoop Bot.
- Administrative actions, such as bans and timeouts, are logged in the server's designated **admin log channel**.
- Records of author identities are automatically deleted (anonymized) after a default period of 30 days.

For more details, please refer to the [Terms of Service](/terms) and [Privacy Policy](/privacy).

## Invite to Your Server

A server administrator can invite the bot by opening the link below. The necessary permissions (View Channels, Send Messages, Attach Files, Timeout Members) are pre-selected for the invitation. **[Invite Link](https://discord.com/oauth2/authorize?client_id=1552626227964018758&scope=bot+applications.commands&permissions=1099511663616
)**

After inviting the bot, a server administrator needs to configure it just once:

1. `/bamboo-setup modrole` - Specify the role authorized to use moderation buttons (select from the dropdown).
2. `/bamboo-setup modlog` - Specify the channel where moderation logs will be recorded (optional).
3. `/bamboo-setup cooldown` - Specify the sending interval in seconds per user (optional; set to 0 to disable).

## How to Use

### Sending Anonymous Messages

1. Type `/bamboo` in the channel where you want to post anonymously.
2. Enter the content in the input window that appears:
- **Message** - The text to send (max 2,000 characters).
- **Media** - Photos, videos, or audio files (max 10 files, up to 10MiB per file).
3. **Submit** - The bot posts the anonymous message to the channel and provides a link via a confirmation message visible only to you.

You can include either text, files, or both. A cooldown may apply if the same user sends messages too rapidly in succession.

### Moderator Features

These features are accessed via buttons on the posted anonymous message. They work only for members with the designated moderator role or the **Manage Messages** permission.

- **View Author** - Check who sent the message (visible only on your screen).
- **Manage** → **Timeout** - Apply a Discord timeout (1 hour to 28 days).
- **Manage** → **Permanent Ban** - Block the user from using the Daesoop Bot.
- **Manage** → **Cancel** - Close without taking action.

You can also manage messages using commands:

| Command | Description |
|---|---|
| `/bamboo-mod block <user> [reason]` | Pre-emptively block a user |
| `/bamboo-mod unblock <user>` | Unblock a user |
| `/bamboo-mod blocked` | View the block list |

## Source Code

Daesoopbot is open-source (GPL-3.0).

- Code repository: [github.com/wb1016/bamboozleify-bot](https://github.com/wb1016/bamboozleify-bot)
- Repository for this page: [github.com/wb1016/daesoopbot-info](https://github.com/wb1016/daesoopbot-info)

Please submit bug reports or feature suggestions via the Issues section of the code repository.
