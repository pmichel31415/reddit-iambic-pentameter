from __future__ import print_function, division

import yaml


class Attributes(object):
    """A class to access dict fields like object attributes"""

    def __init__(self, dic):
        self.__dict__.update(dic)


def load_config(obj, config_file):
    """Create fields from yaml file"""
    with open(config_file, 'r') as f:
        data = yaml.load(f)
        for k, v in data.items():
            obj.__dict__[k] = Attributes(v)
