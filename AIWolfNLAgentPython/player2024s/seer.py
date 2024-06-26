import configparser
import json
import player2024s
import lib

class Seer(player2024s.agent.Agent2024s):
    def __init__(self, inifile:configparser.ConfigParser, name:str) -> None:
        super().__init__(inifile=inifile, name=name)
    
    def parse_info(self, receive: str) -> None:
        return super().parse_info(receive)
    
    def get_info(self):
        super().get_info()
    
        print("\n")
        print(f"myRole: {type(self)}")
        print(f"gameInfo: {self.gameInfo}")
        print(f"gameSetting: {self.gameSetting}")
        print(f"request: {self.request}")
        print(f"talkHistory: {self.talkHistory}")
        print(f"whisperHistory: {self.whisperHistory}")

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