"""
    libkplug, a plugin system for python applications

    Copyright (C) 2013 Kegan Holtzhausen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import yaml
import os
import logging

__author__ = 'Kegan Holtzhausen <marzubus@gmail.com>'

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
                 load_yaml=True, config_load_locations=["."], **kwargs):

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

            # if not os.path.exists(self.config_file):
            for location in config_load_locations:
                if not os.path.exists("%s/%s" % (location, self.config_file)):
                    continue

                self.config_file = "%s/%s" % (location, self.config_file)

                #logging.error("No config file present: %s" % self.config_file)
                #raise FileNotFoundError("no config file present: %s" % self.config_file)

            logging.info("Loading yaml file: %s" % self.config_file)
            stream = open(self.config_file, 'r')
            yaml_settings = yaml.safe_load(stream)

            # get the real values if any
            for variable in yaml_settings.keys():
                logging.debug("Setting config %s = %s" % (variable, yaml_settings[variable]))
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
            logging.debug("Attempting to load plugin: %s" % p)
            try:
                __import__(p, globals())
            except Exception as e:
                logging.error("Failed to import plugin %s" % p)
                raise

        if self.yaml_loaded is False and load_yaml:
            msg = "Failed to find config file: %s in locations: %s" % (config_filename, config_load_locations)
            logging.error(msg)
            raise Exception(msg)

        logging.debug("Config: %s" % self.config)

    def __getattr__(self, item):
        try:
            return self.config[item]
        except KeyError as e:
            logging.error(e)
            logging.error(self.config)
            raise
