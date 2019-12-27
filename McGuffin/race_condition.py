#! python
#
# This is a file for my own learning - dealing with race conditions in
# threading
import concurrent.futures
import logging
import threading
import time

logger = logging.getLogger('TestScript')
formatter = logging.Formatter('(%(levelname)s) - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def thread_function(name):
    logging.info(f"Thread {name}")


class FakeDatabase:
    # The purpose of this class is to serve as a "shared resource" for the
    # program to encounter a race condition over
    def __init__(self):
        self.value = 0

    def update(self, name):
        logging.info(f"Thread {name}: starting update")
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        logging.info(f"Thread {name}: finishing update")


if __name__ == "__main__":
    database = FakeDatabase()
    logging.info(f"Testing update. Starting value is {database.value}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.update, index)
    logging.info("Testing update. Ending value is {database.value}")