import os
import time

import telegram
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

result = set()


def get_api_answer():
    url = "https://polkadot.subscan.io/api/scan/events"
    data = {"row": 100, "page": 0}
    answer = requests.post(url, json=data)
    answer = answer.json()["data"]["events"]
    for i in answer:
        event = i["event_id"]
        extrinsic = "https://polkadot.subscan.io/extrinsic/" + i["extrinsic_hash"]
        if event in ["Bonded", "Unbonded", "Withdrawn"] and extrinsic not in result:
            for j in i["params"].split('"'):
                if j.isnumeric():
                    value = str(round(float(j) / 10 ** 10, 2))
            result.add(extrinsic)
            send_message(extrinsic, event, value)


def send_message(link, event, value):
    message = event + ": " + value + " DOT\n" + link
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    return bot.send_message(chat_id=CHAT_ID, text=message)


if __name__ == "__main__":
    while True:
        time.sleep(60)
        get_api_answer()
