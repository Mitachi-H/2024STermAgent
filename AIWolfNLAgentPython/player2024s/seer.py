import configparser
import json
import player2024s
import lib
from player2024s.info_types import DivineResult
from typing import List

class Seer(player2024s.agent.Agent2024s):
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile, name=name)
        self.divine_results: List[DivineResult] = []
    
    def parse_info(self, receive: str) -> None:
        return super().parse_info(receive)
    
    def get_info(self):
        super().get_info()

        game_info = self.gameInfo
        if game_info is None:
            return 
        divine_result = game_info["divineResult"]
        if divine_result is None:
            return
        
        if divine_result["day"] not in [existing_divine["day"] for existing_divine in self.divine_results]:
            self.divine_results.append(divine_result)

        return
    
    def initialize(self) -> None:
        return super().initialize()
    
    def daily_initialize(self) -> None:
        return super().daily_initialize()
    
    def daily_finish(self) -> None:
        return super().daily_finish()
    
    def get_name(self) -> str:
        return super().get_name()
    
    def get_role(self) -> str:
        return super().get_role()
    
    def talk(self) -> str:
        return super().talk()

    def update_predictions(self):
        self.predictions.update(self.stances, self.divine_results)
    
    def vote(self) -> str:
        return super().vote()
    
    def whisper(self) -> None:
        return super().whisper()

    def divine(self) -> str:
        data = {"agentIdx":lib.util.random_select(self.alive)}

        return json.dumps(data,separators=(",",":"))
    
    def action(self) -> str:

        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()