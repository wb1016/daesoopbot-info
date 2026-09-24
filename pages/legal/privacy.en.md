# bamboozleify-bot Privacy Policy

**Effective date: 2026-09-24**

bamboozleify-bot (Korean name: 대숲봇, the "Bot") is an anonymous message relay service within Discord. This document describes what account data the Bot processes, for what purpose, how long it is kept, and your rights.

## 1. Data We Collect

The Bot stores the following in a database managed by the Bot operator:

| Data | Description | Purpose |
|---|---|---|
| Discord user ID | The unique snowflake ID of the anonymous message author | Handling "See OP" requests from moderators, block management |
| Discord server / channel / message IDs | Identifies where an anonymous message was posted | Linking authors to messages, data management |
| Post timestamp | When the anonymous message was created | Retention management, audit records |
| Submitted content | Text and attachments the User submitted | Posting to the channel as requested |
| Cooldown records | Timestamp of the last post | Spam prevention |
| Block records | Blocked user ID, reason, acting moderator ID, time | Block management and moderation audit |

The Bot also processes transient interaction data Discord delivers with each interaction (command usage, button clicks). This is part of how Discord works; the Bot does not store it separately.

## 2. Data We Do NOT Collect

- IP addresses, email addresses, phone numbers, or other Discord account details
- Normal chat messages the Bot did not post (the Bot does not use the message content intent)
- Cookies, ad tracking, or analytics (the Bot runs no web service)
- Passwords, payment information, or any other personal data

## 3. Purposes of Processing

1. Posting anonymous messages and confirming delivery
2. Supporting Server Moderator actions (author reveal, timeout, block) and their audit trail
3. Spam and flood prevention (cooldowns)
4. Diagnosing service errors

The Bot does not process personal data beyond these purposes, and never for advertising or marketing.

## 4. Storage Location and Retention

1. Data is stored in a SQLite database on a server operated on Oracle Cloud infrastructure in a Korean region (South Korea).
2. **The author's user ID for each anonymous message is deleted (anonymized) from the database after 30 days by default.** After that, the Bot can no longer identify the author of that message.
3. The posted message body and attachments are stored on Discord's servers and remain there until deleted by the server's moderators. The Bot does not keep its own copy.
4. Block records are kept until the block is lifted.

## 5. Sharing and Disclosure

1. The Bot never sells personal data or shares it with third parties for advertising.
2. **Disclosure to Server Moderators:** Author information for an anonymous message is shown only to the Server Moderator who clicks "See OP", only transiently (as an ephemeral message). Moderation actions (timeouts, blocks) may be recorded in the server's designated moderation log channel.
3. If law enforcement or other authorities make a lawful request, information may be provided to the extent required by applicable law.
4. The Bot operates on the Discord platform; Discord Inc.'s own processing of your data is governed by Discord's privacy policy.

## 6. Your Rights

You may request the following regarding your personal data:

1. Access, correction, deletion, or suspension of processing
2. Immediate anonymization of your anonymous-message records (even before the retention period expires)

To make a request: contact `cobaltdev@sudden.ninja` or the moderators of your Discord server. Server-scoped data (e.g., block records) is managed by that server's moderators, so server-related requests are fastest through them.

## 7. Users Under 14

Under Korean law, the Bot cannot obtain consent to collect or process personal data from users under 14 years of age. If you are under 14, you must not use the Bot.

## 8. Changes to This Policy

Changes to this policy take effect immediately when the revised document is published. Material changes will be announced through reasonable means, such as the [Bot's announcement channel](https://github.com/wb1016/daesoopbot-info/blob/main/legal/privacy.en.md).

## 9. Contact

Privacy inquiries: `cobaltdev@sudden.ninja`
