import yaml
import os
import logging

__author__ = 'keghol'

logging = logging.getLogger(__name__)


class KSettings:
    """
    Instantiate a settings object with each kwarg representing a "default".

    The settingsloader searches for a config.yaml file in:

        - config.yaml
        - ${LIBKCONFIG}

    The environment variable: :envvar:`LIBKCONFIG` can also be used to specify another file. e.g

        LIBKCONFIG="/tmp/my.yaml" ...


    :param config_filename: The default filename to check for
    :param config_filename_envvar: The environment variable name which sets filenames to load
    :param export_global: Export config to globals
    :param load_yaml_file: Load from file. If False, only defaults passed in as kwargs are set.
    :param kwargs: Default keys to set


    Examples:

        >>> import libksettings
        >>> settings = libksettings.KSettings(A="boo", B=2, C=True, PLUGINS=[])
        >>> settings.A
        'boo'

    """

    yaml_loaded = False

    # defaults which are set / could not be present
    defaults = {}
    config = {}
    config_file = ""

    def __init__(self, config_filename='config.yaml', config_filename_envvar='LIBKCONFIG', export_global=True,
                 load_yaml=True, **kwargs):

        # copy kwargs into "defaults"
        for k, v in kwargs.items():
            self.defaults[k] = v

        # set the defaults
        for default in self.defaults:
            logging.info("Setting default %s = %s" % (default, self.defaults[default]))
            if export_global:
                globals()[default] = self.defaults[default]
            self.config[default] = self.defaults[default]

        if load_yaml:
            try:
                self.config_file = os.getenv(config_filename_envvar, default=config_filename)
            except Exception as e:
                logging.error("%s: unable to location config file: %s" % (e, self.config_file))
                logging.error(e)

            if not os.path.exists(self.config_file):
                logging.error("No config file present: %s" % self.config_file)
                raise FileNotFoundError("no config file presend: %s" % self.config_file)

            logging.info("Loading yaml file: %s" % self.config_file)
            stream = open(self.config_file, 'r')
            yaml_settings = yaml.load(stream)


            # get the real values if any
            for variable in yaml_settings.keys():
                logging.info("Setting config %s = %s" % (variable, yaml_settings[variable]))
                if export_global:
                    globals()[variable] = yaml_settings[variable]
                self.config[variable] = yaml_settings[variable]

            self.yaml_loaded = True
            logging.info("Yaml loaded successful")
        else:
            logging.info("YAML loading disabled")

        # TODO FIXME
        # get each plugins "default" variables and add to globals

        # warn if plugins not set, probably should move this to libkplug
        if 'PLUGINS' not in kwargs and 'PLUGINS' not in self.config:
            logging.warning("no plugins will be loaded, because missing kwarg 'PLUGINS', e.g PLUGINS=['foo', 'bar']")
        else:
            logging.info("Plugins to load: %s" % self.config['PLUGINS'])

        for p in self.config['PLUGINS']:
            logging.info("Attempting to load plugin: %s" % p)
            try:
                __import__(p, globals())
            except Exception as e:
                logging.error("Failed to import plugin %s" % p)
                raise

        if self.yaml_loaded is False and load_yaml:
            msg = "Failed to find config file"
            logging.error(msg)
            raise Exception(msg)

        logging.info("Config: %s" % self.config)

    def __getattr__(self, item):
        try:
            return self.config[item]
        except KeyError as e:
            logging.error(e)
            logging.error(self.config)
            raise
