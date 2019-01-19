import pkg_resources

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    import subprocess
    __version__ = subprocess.Popen(['git', 'describe'], stdout=subprocess.PIPE).communicate()[0].rstrip()

__author__ = 'Kegan Holtzhausen <Kegan.Holtzhausen@kindredgroup.com>'


# registering the plugin system
from libkplug import KPlugin

# the plugin registry instance
plugin_registry = KPlugin()