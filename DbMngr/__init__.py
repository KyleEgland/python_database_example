#! python
#
# __init__.py <= DbMngr
# This module is responsible for handling database models, relationships, and
# interations
from datetime import datetime
import logging
import os
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
import sys


# ------------------------ #
# ----- Logger Setup ----- #
# ------------------------ #
# Check for the existence of a 'logs' folder - should one not exist, create it
if os.path.exists('./logs/'):
    pass
else:
    try:
        os.mkdir('./logs/')
    except Exception as e:
        print('[-] Unable to create directory - please check permissions')
        sys.exit()
#
# LOGGER creation
logger = logging.getLogger(__name__)
#
# LOGGER set level: Debug -> Info -> Warning -> Error -> Critical
logger.setLevel(logging.DEBUG)
#
# FORMATTER creation
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    datefmt='%d-%b-%Y %H'
)
#
# FILE HANDLER creation
file_handler = logging.FileHandler('./logs/{}.log'.format(__name__))
#
# FILE HANDLER set formatter
file_handler.setFormatter(formatter)
#
# FILE HANDLER set level
file_handler.setLevel(logging.ERROR)
#
# STREAM HANDLER creation
stream_handler = logging.StreamHandler()
# STREAM HANDLER set formatter
stream_handler.setFormatter(formatter)
# STREAM HANDLER set level
stream_handler.setLevel(logging.DEBUG)
#
# LOGGER add handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# NOTES:
# use logger.exception() to get the traceback in addtion to log message
# ---------------------- #
# ----- End Logger ----- #
# ---------------------- #


# Instantiate an instance of the base to be used
Base = declarative_base()


class TimestampMixin(object):
    # Mixin class for use with other models. Provides a created column and
    # updated column to track changes to an entry
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)


class User(TimestampMixin, Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(25))

    def __repr__(self):
        return f"<User: {self.name} created: {self.created}"


if __name__ == "__main__":
    # Some imports for testing
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Giving the database a name here for re-use
    db_name = "db_test.sqlite"

    # Removing previously existing test DB
    if os.path.exists(db_name):
        logger.info
        os.remove(db_name)

    # Create an engine
    engine = create_engine('sqlite:///' + db_name)

    # Create a session connection to the database via the engine
    Session = sessionmaker()
    session = Session.configure(bind=engine)

    # Build the database
    Base.metadata.create_all(engine)
