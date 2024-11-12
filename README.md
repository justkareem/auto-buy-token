# New Coin Notifier

This Python script fetches newly listed coins from a specific API, filters them by a given creator ID, and sends the coin details to a designated Telegram channel using a bot.

## Features

- Fetches newly listed coins every 5 seconds.
- Filters coins by a specific creator.
- Sends a Telegram message with coin details (name, symbol, description, market cap, etc.) to a specified chat or channel.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- A Telegram bot (created via [BotFather](https://t.me/BotFather))
- A Telegram channel or group for receiving notifications

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/new-coin-notifier.git
    cd new-coin-notifier
    ```

2. **Install required libraries**:

    ```bash
    pip install requests
    ```

3. **Set up environment variables**:

    Configure the following environment variables:

    - `TELEGRAM_TOKEN`: Your Telegram bot token.
    - `TELEGRAM_CHAT_ID`: Your Telegram chat or channel ID.

   ### On Windows

   Open Command Prompt as Administrator and set the environment variables using `setx`:

    ```cmd
    setx TELEGRAM_TOKEN "your_telegram_bot_token"
    setx TELEGRAM_CHAT_ID "your_telegram_chat_id"
    ```

   After setting these variables, restart your Command Prompt or IDE for the changes to take effect.

   ### On Unix-based Systems (Linux/macOS)

   You can set these in your terminal session like so:

    ```bash
    export TELEGRAM_TOKEN="your_telegram_bot_token"
    export TELEGRAM_CHAT_ID="your_telegram_chat_id"
    ```

## Usage

Run the script to start fetching and sending notifications:

```bash
python main.py
