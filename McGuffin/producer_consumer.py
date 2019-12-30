#! python
#
# This is a solution to the race-condition issue presented in
# "race_condition.py" - it is using the Producer-Consumer analogy with Lock
import concurrent.futures
import logging
import random
import threading


# Logger setup
logger = logging.getLogger('ProducerConsumer')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s: (%(levelname)s) %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


SENTINEL = object()


def producer(pipeline):
    # The producer is something that, for example, will listen for messages on
    # the network - they may come at any pace anytime.  This function is for
    # simulating that producer - pretend we're getting messages from the
    # network
    for index in range(10):
        message = random.randint(1, 101)
        logger.info(f"FUNC PRODUCER got message: {message}")
        pipeline.set_message(message, "Producer")

    # Send a sentinel message to tell consumer we're done
    pipeline.set_message(SENTINEL, "Producer")


def consumer(pipeline):
    # The consumer is something that, for example, will write messages to a db
    # that are recieved in from the producer.  Imagine that, for this example,
    # we're saving the messages into a db
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            # This is the "writing-to-database" action - we're simply going to
            # log it to console
            logger.info(f"FUNC CONSUMER storing message: {message}")


class Pipeline:
    # This class will pass a single element pipeline between the producer
    # and the consumer functions
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        # Grabbing the consumer_lock here produces the desired starting state:
        # the producer can send a message and the consumer has to wait for a
        # message to be sent.  This sets the stage for beginning the program.
        self.consumer_lock.acquire()

    def get_message(self, name):
        # This is the method by the which the consumer is allowed to get the
        # message set by the producer.
        logger.debug(f"{name}: about to acquire getlock")
        # Acquiring the consumer lock allows the consumer to access the message
        self.consumer_lock.acquire()
        logger.debug(f"{name}: has getlock")
        # Copying in the message
        message = self.message
        logger.debug(f"{name}: about to release setlock")
        # Releasing the producer_lock will now allow the producer to set the
        # next message
        self.producer_lock.release()
        logger.debug(f"{name}: setlock released")
        # Returning the copied message to the caller - we're doing this because
        # calling .release() will immediately allow (like, before the function
        # returns) the message to be changed
        return message

    def set_message(self, message, name):
        # This is (basically) the reverse of get_message
        logger.debug(f"{name}: about to acquire setlock")
        # Acquiring the producer_lock allows the producer to set a message
        self.producer_lock.acquire()
        logger.debug(f"{name}: has setlock")
        # Set the class message value to the input message value sent by the
        # producer
        self.message = message
        logger.debug(f"{name}: about to release getlock")
        self.consumer_lock.release()
        logger.debug(f"{name}: getlock released")


if __name__ == "__main__":
    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
