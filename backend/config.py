import os
from configparser import ConfigParser


class ConfigFile():
    def __init__(self):
        self.config_dir = os.path.dirname(os.path.abspath(__name__))
        self.config_file = "alinka.ini"
        self.config = ConfigParser()

    def read(self):
        init = {}
        self.config.read(os.path.join(self.config_dir, "alinka.ini"))
        sections = self.config.sections()

        for section in sections:
            for option in self.config.options(section):
                init[option] = self.config.get(section, option)
        return init

    def save(self, init):
        file = open(os.path.join(self.config_dir, "alinka.ini"), 'w')
        if 'Center' not in self.config.sections():
            self.config.add_section('Center')
        for option, value in init.items():
            self.config.set('Center', option, value)
        self.config.write(file)
        file.close()
