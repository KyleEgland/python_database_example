#! python
#
# __init__.py <= McGuffin
# This file (and the others inside this directory) borrow heavily/directly from
# "An Intro to Threading in Python" by Jim Anderson. Please see README in the
# root of this project for links (Credits).  Here we're building a bs app that
# will use an actual database - the examples in the source this is derrived
# from used a fake database, here we'll use a real one.
import concurrent.futures
import logging
import queue
import random
import threading
import time


# Logger setup
logger = logging.getLogger('McGuffin')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s: (%(levelname)s) %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def producer(queue, event):
    # Because this is still example code, we'll still be generating fake data.
    # The producer is something that would receive a message (I.e. from the
    # network) and pass it off to a consumer that would write it to a database
    # (or some other function that we'd want done with the information given).
    while not event.is_set():
        message = random.randint(1, 101)
        logger.info(f"Producer got message: {message}")
        queue.put(message)

    logger.info("Producer received event. Exiting...")


def consumer(queue, event):
    # The consumer here is writing out the message information received from
    # the producer.  Here, we'll be writing each message to a database
    while not event.is_set() or not queue.empty():
        message = queue.get()
        logger.info(
            f"Consumer storing message: {message} (size={queue.qsize()})"
        )

    logger.info("Consumer received event. Exiting")


if __name__ == "__main__":

    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logger.info("Main: about to set event")
        event.set()
