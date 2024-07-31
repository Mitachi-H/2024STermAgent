import configparser
import json
import player2024s
import lib
from player2024s.info_types import DivineResult
from typing import List

from player2024s.dev_functions.log import log

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

        log(self.index, ["--update predictions--"])
        for predict_role in self.predictions.predict_roles:
            log(self.index, [f"{predict_role.agent_id} - {predict_role.role} - {predict_role.reason}"])
        log(self.index, ["-----"])
    
    def vote(self) -> str:
        return super().vote()
    
    def whisper(self) -> None:
        return super().whisper()

    def divine(self) -> str:
        # 占う対象の集合 = 生きている + まだ占っていない + 自分でない
        reasonable_divine_targets = [int(agent_id) for agent_id in self.alive if int(agent_id) != self.index and int(agent_id) not in [divine_result["target"] for divine_result in self.divine_results]]
        data = {"agentIdx":lib.util.random_select(reasonable_divine_targets)}

        return json.dumps(data,separators=(",",":"))
    
    def action(self) -> str:

        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()