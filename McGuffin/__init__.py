#! python
#
# This is the "thing do-er" for the demo application project "Python Database
# Example".  Since I like to maximize my time I'm re-creating a project
# derrived from Jim Anderson's article "An Intro to Threading in Python"
# which can be found at https://realpython.com (see Credits section in README)
from datetime import datetime
import logging
import platform
import psutil


logger = logging.getLogger('MyApp.McGuffin')


def get_sys():
    # This is an arbitrary function to do work that will get used by threading
    logger.info('[get_sys] called...')
    pltfrm = platform.uname()
    phys_cores = psutil.cpu_count(logical=False)
    total_cores = psutil.cpu_count(logical=True)
    current_usage = psutil.cpu_percent()
    response = str(
        ':---System Information---:\n'
        f'System: {pltfrm.system}\n'
        f'Node Name: {pltfrm.node}\n'
        f'Release: {pltfrm.release}\n'
        ':---CPU Info---:\n'
        f'Physical cores: {phys_cores}\n'
        f'Total cores: {total_cores}\n'
        f'Current Usage: {current_usage}%\n'
    )
    return response


# Test execution - running this file by itself will invoke the below
if __name__ == '__main__':
    # Setup debug log handling - output to console
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('(%(levelname)s) - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # Let user know that this file is running as __main__
    logger.debug('[+] Debugging McGuffin...')

    sys_info = get_sys()

    print(sys_info)
