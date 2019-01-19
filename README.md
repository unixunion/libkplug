# libkplug

libkplug is a simple framework for creating pluggable python applications. 

It provides a simple framework for loading config from YAML, and then instantiating objects based
off configuration.

example:

```python
# import libkplug before settings
import libkplug
from libksettings import KSettings

# initialize settings with some default
settings = KSettings(MY_HELLO_WORLD_CLASS='HelloWorldPlugin', PLUGINS=['plugins.plugin_helloworld'])

# get the class of the plugin
clazz = libkplug.plugin_registry(settings.MY_HELLO_WORLD_CLASS)

# instantiate it passing in the settings object
inst = clazz(settings=settings)

while True:
    pass
```