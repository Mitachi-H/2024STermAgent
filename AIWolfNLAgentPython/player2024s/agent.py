import json
import configparser
from player.agent import Agent
from player2024s.stance import Stance
from player2024s.my_tactics import MyTactics
from player2024s.predict_role import Predictions

from player2024s.functions.generate_statement import generate_statement

from player2024s.info_types import GameInfo, TalkHistory
from typing import Union

class Agent2024s(Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        super().__init__(inifile, name)

        # ゲーム状況
        self.day: int = 0

        # 考察Class
        self.my_tactics = MyTactics()
        self.stances = []
        self.predictions = None

        if name == "kanolab1":
            print("Agent2024s.__init__", name)

    def get_info(self):
        data = json.loads(self.received.pop(0))

        self.gameInfo: Union[None, GameInfo] = data["gameInfo"] 
        self.gameSetting = data["gameSetting"]
        self.request = data["request"]
        self.talkHistory: TalkHistory = data["talkHistory"]
        self.whisperHistory = data["whisperHistory"]
    
    def initialize(self):
        """
        initializeを受け取ったタイミングで実行されるmethod
        """
        super().initialize()
        # 考察Classの初期化
        self.init_stances()
        self.init_predictions()
    
    def daily_initialize(self):
        # self.alive は 生きてるagentのagentIdのリスト
        super().daily_initialize()

        for stance in self.stances:
            stance.update_alive(int(stance.agent_id) in self.alive)
        self.predictions.update_alive(self.alive)

        day:int = int(self.gameInfo["day"])
        self.day = day
    
    def talk(self) -> str:
        # 他人のスタンスの更新
        self.update_stances()
        # 他人の予想役職の更新
        self.update_predictions()
        # 自分の戦略の更新
        self.update_my_tactics()
        # 発言
        return self.generate_statement()

    def update_stances(self):
        for stance in self.stances:
            stance.update(self.day, self.talkHistory)
    
    def update_predictions(self):
        self.predictions.update(self.stances)

    def update_my_tactics(self):
        self.my_tactics.update(self.day, self.stances, self.predictions)

    def generate_statement(self):
        return generate_statement(self.talkHistory, self.my_tactics)
        
    def init_stances(self):
        """
        initializeを受け取ったタイミングで実行
        """
        statusMap = self.gameInfo["statusMap"]
        self.stances = [Stance(f"{int(agentId):02d}") for agentId in statusMap.keys()]

    def init_predictions(self):
        """
        initializeを受け取ったタイミングで実行
        """
        statusMap = self.gameInfo["statusMap"]
        self.predictions = Predictions(statusMap)
    
    def hand_over(self, new_agent) -> None:
        super().hand_over(new_agent)
        new_agent.my_tactics = self.my_tactics
        new_agent.stances  = self.stances 
        new_agent.predictions = self.predictions
        new_agent.day = self.day