# 🤖 Highrise Bot

![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Highrise](https://img.shields.io/badge/Highrise-Bot-orange?style=for-the-badge)

**The ultimate companion for your Highrise room.**

This bot is a powerful, all-in-one solution designed to enhance your Highrise experience. Whether you need robust moderation tools to keep your room safe, an engaging economy system to reward your visitors, or fun interactive features to keep the party going, this bot has it all.

<img width="1920" height="1440" alt="311_1x_shots_so" src="https://github.com/user-attachments/assets/9e7a18cc-4cfb-418f-9861-6abf54794881" />
---

## ✨ Key Features

| Feature                    | Description                                                                                                                                                                |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **🛡️ Advanced Moderation** | Keep your room safe with powerful tools like **Kick**, **Ban**, **Mute**, and **Unban**. Includes permission checks to ensure only authorized users can moderate.          |
| **💰 Economy System**      | Engage users with a full-fledged economy. Users can **Tip** the bot, check their **Balance**, and earn **VIP status** automatically by reaching tipping thresholds.        |
| **🎭 Interactive Fun**     | Bring your room to life! Access over **50+ Emotes** (with looping support), **Reactions**, **Duet interactions** (Hug, Fight, etc.), **Jokes**, **Quotes**, and **Facts**. |
| **🚀 Utility & Tools**     | Simplify room management with **Custom Teleports** (create your own warp points!), **Reminders** (never forget an event), and **User/Room Info** commands.                 |
| **⚙️ System Integrations** | Stay connected with **Discord Webhook Logging** for chat and events, **Auto-reconnect** for 24/7 uptime, and a built-in **Web Server** for keep-alive monitoring.          |

---

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.10** or higher installed on your system.
- A **Highrise Account** and a **Bot Token** (obtained from the Highrise Developer Portal).
- The **Room ID** where you want the bot to deploy.

---

## 🛠️ Installation & Setup

Follow these steps to get your bot up and running in minutes:

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/highrise-bot.git
    cd highrise-bot
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the Bot**
    Open `config.py` and update the settings (see [Configuration](#-configuration) below).

4.  **Run the Bot**
    ```bash
    python run.py
    ```

---

## ⚙️ Configuration

Edit the `config.py` file to customize your bot. **Keep your tokens secret!**

| Variable             | Description                                            | Example                        |
| :------------------- | :----------------------------------------------------- | :----------------------------- |
| `BOT_ID`             | Your Bot's unique Token (API Key).                     | `"3cb2..."`                    |
| `ROOM_ID`            | The ID of the Highrise room to join.                   | `"688d..."`                    |
| `BOT_UID`            | The User ID of the bot account (for tip tracking).     | `"68ae..."`                    |
| `VIP_THRESHOLD`      | Gold amount required to automatically gain VIP status. | `40`                           |
| `WEBHOOK_URL`        | Discord Webhook URL for logging chat/events.           | `"https://discord..."`         |
| `BOT_START_POSITION` | Coordinates where the bot spawns on join.              | `{"x": 16.5, "y": 10.75, ...}` |
| `quickteleport`      | Enable/Disable instant teleportation for users.        | `False`                        |

---

## 📚 Command Reference

### 🛡️ Moderation

| Command          | Description                               | Permission |
| :--------------- | :---------------------------------------- | :--------- |
| `!kick <user>`   | Kicks a user from the room.               | Mod/Owner  |
| `!ban <user>`    | Bans a user from the room.                | Mod/Owner  |
| `!unban <user>`  | Unbans a user.                            | Mod/Owner  |
| `!mute <user>`   | Mutes a user (temporarily prevents chat). | Mod/Owner  |
| `!mod <user>`    | Promotes a user to moderator (bot-level). | Owner      |
| `!summon <user>` | Teleports a user to your location.        | Mod/Owner  |

### 💰 Economy & VIP

| Command             | Description                                          | Permission |
| :------------------ | :--------------------------------------------------- | :--------- |
| `!tip <amount>`     | Tips the bot (adds to your VIP progress).            | Everyone   |
| `!bal`              | Checks your current wallet balance (if implemented). | Everyone   |
| `!vip`              | Checks your VIP status.                              | Everyone   |
| `!givevip <user>`   | Manually grants VIP status to a user.                | Mod/Owner  |
| `!removevip <user>` | Removes VIP status from a user.                      | Mod/Owner  |
| `!viplist`          | Lists all current VIP users.                         | Mod/Owner  |
| `!tax`              | Fun command (collects "tax").                        | Everyone   |

### 🎭 Fun & Emotes

| Command                    | Description                                       | Permission |
| :------------------------- | :------------------------------------------------ | :--------- |
| `!emote <name>`            | Performs a specific emote (e.g., `!emote dance`). | Everyone   |
| `!emotes`                  | Lists all available emotes.                       | Everyone   |
| `!stop`                    | Stops the current emote loop.                     | Everyone   |
| `!fight <user>`            | Initiates a playful fight duet.                   | Everyone   |
| `!hug <user>`              | Initiates a hug duet (if available).              | Everyone   |
| `!joke`                    | Tells a random joke.                              | Everyone   |
| `!quote`                   | Displays an inspiring quote.                      | Everyone   |
| `!fact`                    | Shares an interesting random fact.                | Everyone   |
| `!punch <user>`            | Punches a user (playful).                         | Everyone   |
| `!heart`, `!clap`, `!wave` | Sends a reaction to a user.                       | Everyone   |

### 🚀 Utility & Teleports

| Command                    | Description                                 | Permission    |
| :------------------------- | :------------------------------------------ | :------------ |
| `!tp <user>`               | Teleports you to another user.              | VIP/Mod/Owner |
| `!maketele <name>`         | Creates a custom teleport at your location. | Mod/Owner     |
| `!teleports`               | Lists all custom teleports.                 | Everyone      |
| `!deltele <name>`          | Deletes a custom teleport.                  | Mod/Owner     |
| `!addreminder <min> <msg>` | Sets a recurring reminder.                  | Mod/Owner     |
| `!listreminders`           | Lists all active reminders.                 | Mod/Owner     |
| `!delreminder <id>`        | Deletes a reminder by ID.                   | Mod/Owner     |
| `!help`                    | Displays the help menu.                     | Everyone      |

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or find a bug:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📞 Support

If you encounter any issues or need assistance, please open an issue on GitHub or contact the bot owner in Highrise.

**Enjoy your enhanced Highrise experience!** 🚀
