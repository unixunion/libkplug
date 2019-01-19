# libkplug

libkplug is a simple framework for creating pluggable python applications, which allow for the abstraction, instantiation 
and usage of classes and static methods.

This simple framework is for loading config from YAML, and then instantiating objects based off configuration, passing
in the config into the 'plugins'

Example:

```python
# import libkplug before settings
import libkplug
from libksettings import KSettings

# initialize settings with some defaults, supressing yaml file load
settings = KSettings(MY_HELLO_WORLD_CLASS='HelloWorldPlugin', PLUGINS=['plugins.plugin_helloworld'], load_yaml=False)

# get the class of the plugin
clazz = libkplug.plugin_registry(settings.MY_HELLO_WORLD_CLASS)

# instantiate it passing in the settings object, this runs init on the class
inst = clazz(settings=settings)

while True:
    pass
```

See [example](/example) for more details

The instances of HELLO_WORLD_CLASS then thread and do their work:

```bash
$> python run.py 
__init__.py:157 INFO Initializing plugin architecture
__init__.py:67 INFO Plugin Init: (), {}
__init__.py:55 INFO Loading yaml file: config.yaml
__init__.py:61 INFO Setting default MY_HELLO_WORLD_CLASS = HelloWorldPlugin
__init__.py:61 INFO Setting default PLUGINS = ['plugins.plugin_helloworld']
__init__.py:71 INFO Setting config KEY1 = VAL1
__init__.py:71 INFO Setting config PLUGINS = ['plugins.plugin_helloworld']
__init__.py:71 INFO Setting config MY_HELLO_WORLD_CLASS = HelloWorldPlugin
__init__.py:77 INFO Yaml loaded successful
__init__.py:83 INFO Plugins to load: ['plugins.plugin_helloworld']
__init__.py:86 INFO Attempting to load plugin: plugins.plugin_helloworld
__init__.py:80 INFO Registering Plugin id: HelloWorldPlugin from class: <class 'plugins.plugin_helloworld.HelloWorldPlugin'> 
run.py:22 INFO Starting up
__init__.py:117 INFO OrderedDict([('HelloWorldPlugin', <class 'plugins.plugin_helloworld.HelloWorldPlugin'>)])
__init__.py:118 INFO Module Unknown->run.py:25->HelloWorldPlugin
__init__.py:119 INFO Plugin Request: args: ('HelloWorldPlugin',), kwargs: {}
__init__.py:121 INFO Class: <class 'plugins.plugin_helloworld.HelloWorldPlugin'>
plugin_helloworld.py:16 INFO Instantiating instance of: HelloWorldPlugin args: () and kwargs: {'settings': <libksettings.KSettings object at 0x1094f1358>}
plugin_helloworld.py:38 INFO Thread-1: Sat Jan 19 09:35:24 2019
plugin_helloworld.py:38 INFO Thread-2: Sat Jan 19 09:35:26 2019
plugin_helloworld.py:38 INFO Thread-1: Sat Jan 19 09:35:26 2019

```

## libksettings

KSettings is designed to load yaml files, and kwargs passed to it are the "defaults". 

Example initializing with DEFAULTS only, no config loading
```python
>>> from libksettings import KSettings
>>> settings = KSettings(A='a', b=1, c=True, PLUGINS=['plugins.plugin_helloworld'], load_yaml=False)
>>> settings.A
'boo'
>>> settings.B
1
```

Example initializing with DEFAULTS and named config file.

```python
>>> from libksettings import KSettings
>>> settings = KSettings(config_filename='/tmp/config.yaml' A='a', b=1, c=True, PLUGINS=['plugins.plugin_helloworld'])
>>> settings.A
'boo'
>>> settings.B
1
```

Example initializing with DEFAULTS and config file from env var

```python
>>> import os
>>> from libksettings import KSettings
>>> os.environ.setdefault('MY_CONF', '/tmp/other.yaml')
>>> settings = KSettings(config_filename_envvar='MY_CONF' A='a', b=1, c=True, PLUGINS=['plugins.plugin_helloworld'])
>>> settings.A
'boo'
>>> settings.B
1
```

