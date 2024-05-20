import json
import configparser
from player.agent import Agent

class Agent2024s(Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        super().__init__(inifile, name)
        if name == "kanolab1":
            print("Agent2024s.__init__", name)

    def get_info(self):
        super().get_info()
        