# It016Bot

A Telegram bot designed to streamline access to study materials for students, making educational resources readily available in one convenient location.

## Motiviation

During the pandemic many universities started reling on online tutoring using tools like Zoom, Google Meet, Telegram, Youtube, ..etc. It016 then started as a project for IT students at UofK to help gather dispersed materials in a single place that is easy to reach and search through.

## Quick start

First of all, make sure to created your bot from [BotFather](https://telegram.me/BotFather). If you don't know how just follow the link and select /newbot, and follow instructions.

Step 1: Clone the Repository:

```bash
git clone https://github.com/aelkheir/it016bot.git
```

Step 2: Install Dependencies:
Navigate to the project directory and run

```bash
pip install -r requirements.py
```

After that you need to create a `.env` and fill in your token and config strings. You can use the file `.env.example` as a template.

Step 3: Start the web server

```bash
flask run
```

Step 4: Start the main end point:
Open your browser and navigate to http://127.0.0.1:5000/!

Now you can go to your bot in Telegram and interact with it.
