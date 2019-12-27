#! python
#
# This is the application which will be utilizing our database management
# module.  This app is really for demonstrative purposes, however, it still
# does a thing.  The thing it does is irrelevant to the purpose of this project
# but feel free to check it out all the same.  The idea here is that the
# program has a default run-state (invoked with no parameters it does a default
# action which is what we'll normally use the app for) along with several
# command line options that allow it to modify the default run-state and allow
# database management (which is the point of this project)
import click


@click.command()
def cli():
    # The below docstring is used in the help print-out created by click
    """Demo Python application - I print stuff :)"""
    click.echo('[+] MyApp is running with default parameters...')


if __name__ == '__main__':
    cli()
