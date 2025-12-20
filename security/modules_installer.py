import os
import time
import importlib
import subprocess
from customs import show
from file_handlers import read_text
from customs import show
from global_constants import ALTERNATE_LOGO_PATH


class security:
    """ Verifies the installlations of all the python pip packages listed in the requirements.txt file"""

    def __init__(self, requirements_file):
        self.__requirements_file = requirements_file

    def check(self):
        try:
            for module in read_text(self.__requirements_file).splitlines():
                module_name = module.split("=")[0]
                globals()[module_name] = importlib.import_module(module_name)
        except Exception as e:
            print("modules aare missing ", e)
            self.install()

    def install(self):
        try:
            subprocess.run(["pip", "install", "-r", "requirements.txt"])
            os.system("clear")
        except Exception as e:
            print(e)

    def clear(self):
        os.system("clear")
