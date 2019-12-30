#! python
#
# This is a file for my own learning - dealing with race conditions in
# threading
import concurrent.futures
import logging
import time

logger = logging.getLogger('RaceCondition')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s: (%(levelname)s) %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class FakeDatabase:
    # The purpose of this class is to serve as a "shared resource" for the
    # program to encounter a race condition over
    def __init__(self):
        self.value = 0

    def update(self, name):
        # Here is where the race-condition is formed - we create a "local" copy
        # of our "database value" which is called by the ThreadPoolExecutor.
        # The executor then creates (2) copies of the same value which will
        # therefore not be reflected properly upon inspection of the value
        # after the change (each func will update 0 to 1 when we expect it to
        # be 2)
        logger.info(f"Thread {name}: starting update")
        local_copy = self.value
        local_copy += 1
        time.sleep(0.1)
        self.value = local_copy
        logger.info(f"Thread {name}: finishing update")


if __name__ == '__main__':
    # Instantiate the simulated database
    database = FakeDatabase()
    logger.info(f"Testing update. Starting value is {database.value}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            # Here we specify the function (database.update method) and what
            # arg we're passing it - doing this creates two local copies of the
            # the function which will each contain the same initial value.
            # This sets us up for the race condition regarding the value we
            # write back.
            executor.submit(database.update, index)
    logger.info(f"Testing update. Ending value is {database.value}")
