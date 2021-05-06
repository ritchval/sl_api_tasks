import os
import time
import logging
import requests
import json
from config.config import config
from time_functions.timer_function import time_function
from notification.discord import send_notification
import database.db_interface as db
from database.Battle import Battle

PLAYER_NAME = config('PLAYER_NAME')
logging.basicConfig(level=logging.INFO, filename=f"{os.path.join(config('LOG_PATH'), 'downloader.log')}",
                    format='%(asctime)s - %(levelname)s - %(message)s')

def request_data():
    return requests.get(f"https://api.splinterlands.io/battle/history?player={PLAYER_NAME}"), requests.get(f"https://api.splinterlands.io/players/details?name={PLAYER_NAME}")


def update_json():

    start = time.perf_counter()
    # Getting the last 50 battles
    battles_response, power_response = request_data()
    logging.info(
        f"The task 'request_data' took {time.perf_counter() - start:0.4f} seconds.")

    # Printing the response of the api server
    logging.info(f"Battle history: {battles_response}")
    logging.info(f"Player details: {power_response}")

    # Loading the JSON string data into a dictionary containing player and battles, which contains a list of dictionaries
    new_data = json.loads(battles_response.text)
    current_power = json.loads(power_response.text)["collection_power"]

    battles_to_add = []

    # add the new battles
    for battle in new_data["battles"]:

        if battle["match_type"] != "Ranked":
            continue

        battles_to_add.append(Battle(battle_queue_id_1=battle["battle_queue_id_1"], battle_queue_id_2=battle["battle_queue_id_2"], player_1_rating_initial=battle["player_1_rating_initial"], player_2_rating_initial=battle["player_2_rating_initial"], winner=battle["winner"], player_1_rating_final=battle["player_1_rating_final"], player_2_rating_final=battle["player_2_rating_final"], details=battle["details"], player_1=battle["player_1"], player_2=battle["player_2"], created_date=battle["created_date"], match_type=battle["match_type"], mana_cap=battle["mana_cap"], current_streak=battle["current_streak"], ruleset=battle["ruleset"], inactive=battle["inactive"], settings=battle["settings"], block_num=battle["block_num"], rshares=battle["rshares"], dec_info=battle["dec_info"], leaderboard=battle["leaderboard"], power=current_power))

    db.add_battles(battles_to_add)


if __name__ == '__main__':
    try:
        update_json()
    except BaseException:
        import sys
        logging.critical(sys.exc_info()[0])
        import traceback
        logging.critical(traceback.format_exc())

        send_notification("Downloader encountered an Error.", 'error')
