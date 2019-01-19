# libkplug

libkplug is a simple framework for creating modular, configuration driven python applications.

Q: How is this different from just standard modular development.

A: The use cases for libkplug stem from a need to name classes to use for specific workloads at a configuration level, 
and load and operate instances of those classes from named methods. .e.g `plugin_registry('some_plugin').my_static_method()` 

Q: How do I instantiate plugins without "knowing" the type

A: Code
```python
# read the class
clazz = libkplug.plugin_registry('SomePluginName')
# instantiate with kwargs
myinst = clazz(key1=1, keyN='N')
```

## Installation

```bash
source /my/venv/bin/activate
python setup.py install
```

## Usage

### Simple Example

This is a simple example, which will load the module `plugins.plugin_helloworld`, which contains a class `HelloWorldPlugin`,
The program then instantiate a instance of the plugin by its name which is a string.

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

The output for the above example:

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


### Sample Application

See [example](/example) which loads a yaml file, and starts a plugin which has two threads.


## libkplug

libkplug provides the plugin_registry, and plugin registration decorators. Example plugin:

```python
import logging

# initializes the plugin system
import libkplug
from libkplug import KPlugin

# a inline plugin registration
@libkplug.plugin_registry.register
class HelloWorldPlugin(KPlugin):
    # this is the identifier for when calling the plugin, should almost always be the class name
    plugin_name = 'HelloWorldPlugin'

    def __init__(self, *args, **kwargs):
        logging.info('Instantiating instance of: %s args: %s and kwargs: %s' % (self.plugin_name, args, kwargs))

    def hello(self, name="default"):
        logging.info("Hello %s from %s instance method" % (name, self))
        return name

    @staticmethod
    def hello_world():
        logging.info("Hello World")
        return "Hello World"

```

### Initialize the Plugin System

```python
>>> # init libkplug
>>> import libkplug
>>> # check current plugins
>>> print(libkplug.plugin_registry.plugins_dict)
OrderedDict()
```

### Register a Plugin with KSettings

```python
>>> import libksettings
>>> import libkplug
__init__.py:157 INFO Initializing plugin architecture
__init__.py:67 INFO Plugin Init: (), {}
>>> settings = libksettings.KSettings(PLUGINS=['plugins.plugin_helloworld'], load_yaml=False)
__init__.py:56 INFO Setting default PLUGINS = ['plugins.plugin_helloworld']
__init__.py:87 INFO YAML loading disabled
__init__.py:96 INFO Plugins to load: ['plugins.plugin_helloworld']
__init__.py:99 INFO Attempting to load plugin: plugins.plugin_helloworld
__init__.py:80 INFO Registering Plugin id: HelloWorldPlugin from class: <class 'plugins.plugin_helloworld.HelloWorldPlugin'> 
__init__.py:111 INFO Config: {'PLUGINS': ['plugins.plugin_helloworld']}
>>> 
```

### Register a Plugin Manually

Importing any file containing classes decorated with `@libkplug.plugin_registry.register` will register the plugins. Just
be sure to import libkplug before.

```python
>>> import libkplug
__init__.py:157 INFO Initializing plugin architecture
__init__.py:67 INFO Plugin Init: (), {}
>>> import plugins.plugin_helloworld
__init__.py:80 INFO Registering Plugin id: HelloWorldPlugin from class: <class 'plugins.plugin_helloworld.HelloWorldPlugin'> 
>>> 

```

### Plugin Static Methods

Static methods work as expected, and do not require instantiation of the plugin, it only needs to be loaded to work.

```python
>>> import libkplug
>>> import plugins.plugin_helloworld
>>> libkplug.plugin_registry('HelloWorldPlugin').hello_world()
'Hello World'
```


### Plugin Instantiation

Instantiation is done by determining the class, and then passing in kwargs to the constructor as usual.

```python
>>> import libkplug
>>> import plugins.plugin_helloworld
>>> # read the class
>>> clazz = libkplug.plugin_registry('HelloWorldPlugin')
>>> # instantiate with kwargs
>>> myinst = clazz(key1=1, keyN='N')
```


## libksettings

KSettings is designed to load yaml files, set defaults, and initialize plugins listed in `PLUGINS`.

IMPORTANT: KSettings is "global", so once instantiated with "defaults" and or a config, any other part of the application
can import KSettings and access previously set values without reloading the config or redefining defaults. That said you
might want to use namespaced defaults if plugins need to declare defaults.

Example of separate instances "sharing" config
```python
>>> import libksettings
>>> settings1 = libksettings.KSettings(A='a', b=1, c=True, PLUGINS=[], load_yaml=False)
>>> settings2 = libksettings.KSettings(load_yaml=False)
>>> settings1.A == settings2.A
True
```

Example if separate instances declaring new defaults
```python
>>> import libksettings
>>> foo_settings = libksettings.KSettings(A='a', b=1, c=True, PLUGINS=[], load_yaml=False, FOO_DEFAULT="foo")
>>> bar_settings = libksettings.KSettings(A='a', b=1, c=True, PLUGINS=[], load_yaml=False, BAR_DEFAULT="bar")
>>> foo_settings.BAR_DEFAULT
'bar'
```

When KSettings is instantiated, it will use all kwargs as 'default' initial values, then load the yaml file, overriding
any defaults, finally it loads the Plugins, and returns a instance of itself.

Example initializing without config file, setting some defaults, and not loading plugins, 
```python
>>> from libksettings import KSettings
>>> settings = KSettings(A='a', b=1, c=True, PLUGINS=[], load_yaml=False)
>>> settings.A
'boo'
>>> settings.B
1
```


Example initializing with DEFAULTS and named config file, and default plugins

```python
>>> from libksettings import KSettings
>>> settings = KSettings(config_filename='/tmp/config.yaml' A='a', b=1, c=True, PLUGINS=['plugins.plugin_helloworld'])
>>> settings.A
'boo'
>>> settings.B
1
>>> settings.SOME_YAML_KEY
'bar'

```

Example initializing with DEFAULTS and named config file from env var

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


