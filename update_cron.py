import os
import logging
import requests
import json
from datetime import datetime, timedelta
from crontab import CronTab

from config.config import config
from time_functions.timer_function import time_function
from notification.discord import send_notification


PLAYER_NAME = config('PLAYER_NAME')
PROJECT_PATH = config('PROJECT_PATH')
PYTHON = os.path.join(PROJECT_PATH, ".venv/bin/python")
NOTIFIER_FILE = os.path.join(PROJECT_PATH, "quest_notifier.py")
USER = config('SYSTEM_USER')

logging.basicConfig(level=logging.INFO, filename=f"{os.path.join(config('LOG_PATH'), 'update_cron.log')}",
                    format='%(asctime)s - %(levelname)s - update_cron - %(message)s')


@time_function("'update quest task time'")
def update_cron():

    my_cron = CronTab(user=USER)

    # job = my_cron.new(
    #     command=f"{PYTHON} {NOTIFIER_FILE}", comment='sl_quest_notifier')
    # job.setall(56, 23, '*', '*', '*')

    sl_response = requests.get(
        f"https://api.splinterlands.io/players/quests?username={PLAYER_NAME}")

    logging.info(f"Splinterlands: {sl_response}")

    # Loading the JSON string data into a dictionary
    quest_data = json.loads(sl_response.text)[0]

    # extract datetime object our of the string
    quest_time = datetime.fromisoformat(
        quest_data['created_date'].replace('Z', ''))

    quest_time += timedelta(hours=25)

    # set the task to the time of next quest
    for job in my_cron:
        if job.comment == 'sl_quest_notifier':
            job.setall((quest_time.minute), quest_time.hour, "*", "*", "*")
            my_cron.write()

            break

    logging.info(
        f"Changed times to {quest_time.hour}:{str(quest_time.minute).zfill(2)}.")


if __name__ == "__main__":
    try:
        update_cron()
    except:
        send_notification("Quest Checker encountered an error.", 'error')
        import sys
        logging.critical(sys.exc_info()[0])
        import traceback
        logging.critical(traceback.format_exc())
