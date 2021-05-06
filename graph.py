import os
import logging
import json
import matplotlib.pyplot as plt
from config.config import config
from notification.discord import send_notification
import database.db_interface as db
from database.Battle import Battle

DATA_PATH = os.path.join(config('PROJECT_PATH'), 'data')
PLAYER = config('PLAYER_NAME')


logging.basicConfig(level=logging.INFO, filename=f"{os.path.join(config('LOG_PATH'), 'graph.log')}",
                    format='%(asctime)s - %(levelname)s - %(message)s')

ratings = []
power_list = []


def generate_lists():

    # get all ratings, name and power
    data_rows = db.fetchall_short()

    # get the ratings and save them to a list
    for data in data_rows:
        ratings.append(data[0] if data[3] == PLAYER else data[1])

        # if the battle has a power value (added 28.01.21) add that
        power_list.append(data[2])

    logging.info(f"Number of ratings: {len(ratings)}")
    # -1303 since i have 1303 battles without power
    logging.info(f"Number of powers: {len(power_list) - 1303}")


def generate_graph():

    plt.figure(figsize=(20, 10))

    ratings_plot = plt.gca()
    power_plot = ratings_plot.twinx()

    ratings_plot.plot(ratings)
    power_plot.plot(power_list, color='red')

    # ymin, ymax = ratings_plot.get_ylim()

    power_plot.set_yticks(
        [1000, 5000, 15000, 40000, 70000, 100000, 150000, 200000])

    ratings_plot.axhline(y=100, color='darkgoldenrod', linestyle=':')
    ratings_plot.axhline(y=400, color='darkgoldenrod', linestyle=':')
    ratings_plot.axhline(y=700, color='darkgoldenrod', linestyle=':')

    ratings_plot.axhline(y=1000, color='gray')
    ratings_plot.axhline(y=1300, color='gray', linestyle=':')
    ratings_plot.axhline(y=1600, color='gray', linestyle=':')

    ratings_plot.axhline(y=1900, color='gold', linestyle='--')

    ratings_plot.set_xlabel('battles')
    ratings_plot.set_ylabel('rating')
    power_plot.set_ylabel('power')
    plt.title('Rating over time')

    # plt.show()
    plt.savefig(os.path.join(DATA_PATH, 'ratings_graph.png'))


if __name__ == "__main__":
    try:
        generate_lists()
        generate_graph()
    except BaseException:
        import sys
        logging.critical(sys.exc_info()[0])
        import traceback
        logging.critical(traceback.format_exc())

        send_notification("Graph creation ecountered an ERROR.", 'error')
