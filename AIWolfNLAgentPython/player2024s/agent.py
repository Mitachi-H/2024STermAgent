import json
import configparser
from ..player.agent import Agent


class Agent2024s(Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        print("Agent2024s.__init__")
        super().__init__(inifile, name)

    def get_info(self):
        super().get_info()
        
        print(f"gameInfo: {self.gameInfo}")
        print(f"gameSetting: {self.gameInfo}")
        print(f"request: {self.request}")
        print(f"talkHistory: {self.talkHistory}")
        print(f"whisperHistory: {self.whisperHistory}")