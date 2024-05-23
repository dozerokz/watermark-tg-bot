# Watermark Bot

This is a Telegram bot that helps you add watermarks to your photos. The bot is completely free to use, and you won't
find any other watermarks on your photos except yours.

## Features

- Add text watermarks to your images
- Adjust watermark transparency
- Support for different watermark positions and sizes
- Easy-to-use interface with buttons
- Receive your watermarked image instantly

## Getting Started

### Prerequisites

Before running the bot, you need to:

1. Create a Telegram bot using [@BotFather](https://t.me/BotFather) and obtain the bot token.
2. Install the required Python packages listed in `requirements.txt`.
3. Set up the environment variable `BOT_TOKEN` with your bot token.

### Installation

1. Clone the repository:

```sh
git clone https://github.com/dozerokz/cd watermark-tg-bot.git
```

2. Install the dependencies:

```sh
cd watermark-tg-bot
pip install -r requirements.txt
```

3. Set Environment Variable:

```sh
export BOT_TOKEN="your_bot_token_here"
```

## Usage

1. Run the bot:

```sh
python3 watermark_bot.py
```

2. Run API (optional)

```sh
python3 api.py
```

3. Start a conversation with your bot on Telegram.

4. Send an image to the bot to start adding watermarks.

5. You can check your bot statistics via http://127.0.0.1:5000/stats

### API

This bot also includes an API for posting data and retrieving statistics.

#### Endpoints

- **Add User**: `POST /users`
    - Request Body: `{"user_id": int}`
    - Response: Adds a new user if it doesn't exist and returns a success message.

- **Add Watermark**: `POST /watermarks`
    - Request Body: `{"user_id": int}`
    - Response: Increments the watermark count for the user and returns a success message.

- **Get Stats**: `GET /stats`
    - Response: Returns the total number of users and total watermarks.

### Bot Commands

- `/start`: Sends a welcome message and instructions to send an image.
- `/help`: Provides detailed instructions on how to use the bot.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
