import logging
import os


class ActivityLogger:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

        logging.basicConfig(
            filename="data/activity.log",
            level=logging.INFO,
            format="%(asctime)s | %(message)s"
        )

    def log(self, message):
        logging.info(message)