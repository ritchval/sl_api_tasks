import os
import logging
from datetime import date
from notification.discord import send_notification
from time_functions.timer_function import time_function
import database.db_interface as db
from config.config import config

logging.basicConfig(level=logging.INFO, filename=f"{os.path.join(config('LOG_PATH'), 'check_activity.log')}",
                    format='%(asctime)s - %(levelname)s - check_activity - %(message)s')


@time_function("'check_activity'")
def check_activity():

    last_played = db.select_newest_date()

    db_date = last_played.split("T")[0]

    if db_date != date.today().isoformat():
        send_notification(
            f"No new games were added today. Last game: {last_played}", 'error')
        logging.warning(f"Have you been playing? Last game: {last_played}")


if __name__ == '__main__':
    try:
        check_activity()
    except BaseException:
        import sys
        logging.critical(sys.exc_info()[0])
        import traceback
        logging.critical(traceback.format_exc())

        send_notification("Downloader encountered an Error.", 'error')
