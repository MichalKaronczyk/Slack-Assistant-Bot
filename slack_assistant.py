import os
import logging
from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
import openai

def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    return logging.getLogger(__name__)

logger = configure_logging()

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.error("Brak OPENAI_API_KEY w .env. Ustaw klucz i restartuj aplikację.")
    exit(1)

openai.api_key = OPENAI_API_KEY

slack_app = App(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)
handler = SlackRequestHandler(slack_app)

server = Flask(__name__)

@server.route('/slack/events', methods=['POST'])
def slack_events():
    return handler.handle(request)

@slack_app.event("app_mention")
def handle_app_mention(body, say):
    logger.info(f"Otrzymano payload: {body}")
    event = body.get("event", {})
    text = event.get("text", "")
    thread_ts = event.get("ts")

    prompt = text.split('>', 1)[-1].strip()
    logger.info(f"Prompt do OpenAI: {prompt}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Jesteś pomocnym asystentem na Slacku."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        say(text=answer, thread_ts=thread_ts)
    except Exception as e:
        logger.error("Błąd przy wywoływaniu OpenAI:", exc_info=True)
        say(text="Ups, coś poszło nie tak. Sprawdź logi.", thread_ts=thread_ts)

if __name__ == "__main__":
    server.run(port=3000)
