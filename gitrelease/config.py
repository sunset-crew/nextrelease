#!/usr/bin/env python3

from pathlib import Path
from configparser import ConfigParser
from os.path import exists
from os import getenv

HOME_LOCATION = str(Path.home())

CONFIG_FILE_LOCATION = getenv("CONFIG_FILE", HOME_LOCATION + "/.gitrelease.conf")

""" An Example of the Config file
[main]
body_separator="-"
title_separator="-"
"""


class Settings(object):
    def __init__(self):
        self.config = {"config": {"title_separator": "-", "body_separator": "-"}}
        if exists(CONFIG_FILE_LOCATION):
            config_parse = ConfigParser()
            config_parse.read(CONFIG_FILE_LOCATION)
            self.config["config"]["body_separator"] = config_parse.get(
                "main", "body_separator"
            ).replace('"', "")
            self.config["config"]["title_separator"] = config_parse.get(
                "main", "title_separator"
            ).replace('"', "")

    def __call__(self):
        return self.config
