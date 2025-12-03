# Highrise Bot

This is a feature-rich bot for the Highrise metaverse platform, built in Python using the `highrise-bot-sdk`.

## Features

*   **Moderation:** Ban, kick, and mute users.
*   **User Interaction:** Jokes, facts, quotes, emotes, and reactions.
*   **VIP System:** Manage VIP users based on tips.
*   **AI Integration:** AI-powered emotes.
*   **External Integrations:** News API and Discord webhook integration.
*   **And much more!**

## Getting Started

### Prerequisites

*   Python 3.10
*   Poetry

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

### Configuration

For security, it is recommended to use environment variables to store your bot's secrets.

1.  **Create a `.env` file** in the root of the project and add the following variables:

    ```
    BOT_ID="your-bot-id"
    ROOM_ID="your-room-id"
    BOT_UID="your-bot-uid"
    NEWS_API_KEY="your-news-api-key"
    HF_API_KEY="your-huggingface-api-key"
    WEBHOOK_URL="your-discord-webhook-url"
    ```

2.  **Install the `python-dotenv` library:**
    ```bash
    poetry add python-dotenv
    ```

3.  **Update `config.py`** to load these variables.
### Usage

To run the bot, use the following command:

```bash
poetry run python main.py
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
