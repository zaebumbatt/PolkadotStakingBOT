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
    data = {"row": 20, "page": 0}
    answer = requests.post(url, json=data)
    answer = answer.json()["data"]["events"]
    for i in answer:
        event = i["event_id"]
        event_index = i["event_index"]
        if event_index not in result and event in ["Bonded", "Unbonded", "Withdrawn"]:
            extrinsic = "https://polkadot.subscan.io/extrinsic/" + i["extrinsic_hash"]
            for j in i["params"].split('"'):
                if j.isnumeric():
                    value = str(round(float(j) / 10 ** 10, 2))
                    break
            result.add(event_index)
            send_message(extrinsic, event, value)


def send_message(link, event, value):
    if float(value) >= 10000:
        message = event + ": " + value + " DOT\n" + link
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        return bot.send_message(chat_id=CHAT_ID, text=message)
    return


if __name__ == "__main__":
    while True:
        time.sleep(60)
        get_api_answer()
