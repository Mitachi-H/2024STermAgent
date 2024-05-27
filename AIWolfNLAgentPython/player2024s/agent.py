import json
import configparser
from player.agent import Agent
from player2024s.stance import Stance
from player2024s.my_tactics import MyTactics
from player2024s.predict_role import PredictRole

from player2024s.info_types import GameInfo, TalkHistory
from typing import Union

class Agent2024s(Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        super().__init__(inifile, name)

        # 考察Class
        self.my_tactics = MyTactics()
        self.stances = []
        self.predict_roles = []

        if name == "kanolab1":
            print("Agent2024s.__init__", name)

    def get_info(self):
        data = json.loads(self.received.pop(0))

        # TODO: GameInfo, TalkHistoryの型変換（dict->class）を実装
        # そのままでも動きそう？
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
        self.init_predict_roles()
    
    def daily_initialize(self):
        # self.alive は 生きてるagentのagentIdのリスト
        super().daily_initialize()
        for stance, predict_role in zip(self.stances, self.predict_roles):
            stance.update_alive(int(stance.agent_id) in self.alive)
            predict_role.update_alive(int(predict_role.agent_id) in self.alive)
    
    def talk(self) -> str:
        # 他人のスタンスの更新
        
        # 他人の予想役職の更新
        # 自分のスタンスの設定
        # 発言
        super().talk()
        
    def init_stances(self):
        """
        initializeを受け取ったタイミングで実行
        """
        statusMap = self.gameInfo["statusMap"]
        self.stances = [Stance(f"{int(agentId):02d}") for agentId in statusMap.keys()]

    def init_predict_roles(self):
        """
        initializeを受け取ったタイミングで実行
        """
        statusMap = self.gameInfo["statusMap"]
        self.predict_roles = [PredictRole(f"{int(agentId):02d}") for agentId in statusMap.keys()]