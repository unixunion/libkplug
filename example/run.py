#!/usr/bin/env python

import os
import sys
import logging

# path modification to be able to run example against src, otherwise wont be able to resolve
sys.path.insert(1, os.path.join(sys.path[0], '../src'))

# initialize the logger before kplug
logging.basicConfig(format='%(filename)s:%(lineno)s %(levelname)s %(message)s', stream=sys.stdout)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.INFO)

# import libkplug before settings
import libkplug
from libksettings import KSettings

# initialize settings with some default
settings = KSettings(MY_HELLO_WORLD_CLASS='HelloWorldPlugin', PLUGINS=['plugins.plugin_helloworld'])

logging.info("Starting up")

# get the class of the plugin
clazz = libkplug.plugin_registry(settings.MY_HELLO_WORLD_CLASS)

# instantiate it passing in the settings object
inst = clazz(settings=settings)

while True:
    pass
