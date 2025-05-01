## Overview
This is a simple Slack assistant built with Python’s Bolt framework and the OpenAI API. It listens for `app_mention` events in your Slack workspace, forwards your prompt to OpenAI’s GPT-3.5-turbo model, and replies in-thread with the generated response. The app runs locally via Flask and is exposed to Slack using ngrok.

## Prerequisites
- **Python 3.6+** installed on your machine.  
- A **Slack workspace** where you can install apps.  
- An **OpenAI API key** (set as `OPENAI_API_KEY`).  
- **ngrok** for exposing your local server to the internet.

## Installation
1. **Clone the repository** and navigate into it:
   ```bash
   git clone <your-repo-url>
   cd Slack-Assistant-Bot
   ```
2. **Create and activate** a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies** (using the stable OpenAI 0.27.0 SDK):
   ```bash
   pip install slack_bolt python-dotenv flask openai==0.27.0
   ```  

## Configuration
1. **Create a `.env`** file in the project root:
   ```ini
   SLACK_BOT_TOKEN=<your_bot_token>
   SLACK_SIGNING_SECRET=<your_signing_secret>
   OPENAI_API_KEY=<your_openai_api_key>
   ```
2. In your **Slack App** settings:
   - Under **OAuth & Permissions**, add Bot Token Scopes:  
     ```
     app_mentions:read
     chat:write
     ```
   - **Event Subscriptions** → Enable and set **Request URL** later (see below).  
   - **Install** or **Reinstall** the app to your workspace so scopes take effect.

## Running with ngrok
1. **Start the Python app** on port 3000:
   ```bash
   python3 slack_assistant.py
   ```
2. **Launch ngrok** in a new terminal to expose port 3000:
   ```bash
   ngrok http 3000
   ```
3. **Configure Slack**:
   - Go to **Event Subscriptions** in your Slack App.  
   - Paste the URL:
     ```
     https://<your-ngrok-id>.ngrok.io/slack/events
     ```
   - Click **Save** and then **Reinstall App**.

## Usage
1. **Invite the bot** to any channel (or DM):
   ```bash
   /invite @YourBotName
   ```
2. **Mention the bot** with your question or prompt. For example:
   ```
   @YourBotName How do I write a for-loop in Python?
   ```
   The bot will send your text to OpenAI and reply in-thread with the answer.

---

You now have a fully functional Slack assistant powered by GPT-3.5, running locally and exposed via ngrok!
