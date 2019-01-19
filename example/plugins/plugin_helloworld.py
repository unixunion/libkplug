
__author__ = 'Kegan Holtzhausen <marzubus@gmail.com>'

import logging
import _thread
import time

# initializes the plugin system
import libkplug
from libkplug import KPlugin


# a inline plugin registration
@libkplug.plugin_registry.register
class HelloWorldPlugin(KPlugin):
    plugin_name = 'HelloWorldPlugin'

    def __init__(self, *args, **kwargs):
        logging.info('Instantiating instance of: %s args: %s and kwargs: %s' % (self.plugin_name, args, kwargs))
        # Create two threads as follows
        try:
            _thread.start_new_thread(self.print_time, ("Thread-1", 2,))
            _thread.start_new_thread(self.print_time, ("Thread-2", 4,))
        except:
            logging.error("Error: unable to start thread")

    def hello(self, name="default"):
        logging.info("Hello %s from %s instance method" % (name, self))
        return name

    @staticmethod
    def hello_world():
        logging.info("Hello World")
        return "Hello World"

    def print_time(self, threadName, delay):
        count = 0
        while count < 5:
            time.sleep(delay)
            count += 1
            logging.info("%s: %s" % (threadName, time.ctime(time.time())))
