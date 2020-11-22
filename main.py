import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

result = {}


def get_api_answer():
    url = "https://polkadot.subscan.io/api/scan/events"
    data = {"row": 100, "page": 0}
    answer = requests.post(url, json=data)
    answer = answer.json()["data"]["events"]
    value = 0

    for i in answer:
        event = i["event_id"]
        if event in ["Bonded", "Unbonded", "Withdrawn"]:
            extrinsic = "https://polkadot.subscan.io/extrinsic/" + i["extrinsic_hash"]
            if result.get(extrinsic):
                continue
            else:
                for j in i["params"].split('"'):
                    if j.isnumeric():
                        value = str(round(float(j) / 10 ** 10, 2))
                result[extrinsic] = [event, value]
                send_message(extrinsic, event, value)


def send_message(link, event, value):
    message = event + ": " + value + " DOT\n" + link
    url = (
            "https://api.telegram.org/bot"
            + TELEGRAM_TOKEN
            + "/sendMessage?chat_id="
            + CHAT_ID
            + "&text="
            + message
    )
    requests.post(url)


if __name__ == "__main__":
    while True:
        time.sleep(300)
        get_api_answer()
