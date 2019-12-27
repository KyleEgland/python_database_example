# Python Database Example
An example of how to handle databases with Python 3

## Synopsis
This project represents more of a design pattern than an actual Python module or "how to".  The idea here is that we have an application of some kind that requires a database connection that is managed as a part of the app.  This scenario presumes that we're developing the database structure alongside the application meaning that there will be changes as the app progresses which will necessitate migrations.  This project will be utilizing Python 3 (3.7.3 to be precise) along with SQLAlchemy, python-dotenv, and Alembic (among others - see `requirements.txt` for full listing of dependencies) to achieve or database needs.

## Setup
Running this project is as simple as pulling the repo, creating a virtual environment, and running the code.

`user@machine: ~/workspace$ git pull https://github.com/KyleEgland/python_database_example.git`

`user@machine: ~/workspace/python_database_example$ python -m virtualenv env`

`user@machine: ~/workspace/python_database_example$ source env/bin/activate`

`(env) user@machin: ~/workspace/python_database_example$ python -m pip install -r requirements.txt`

## Credits
The people, projects, etc. that helped to make this project what it is.  Should you enjoy or get anything out of this project please visit the resources provided below to give them your patronage as well :)

* [SQLAlchemy]("https://www.sqlalchemy.org/")
* [Click]("https://click.palletsprojects.com/")
* ["An Intro to Threading in Python"]("https://realpython.com/intro-to-python-threading/")
    * [Jim Anderson's]("https://realpython.com/team/janderson/")
