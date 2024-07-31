import json
import configparser
from player.agent import Agent
from player2024s.stance import Stance
from player2024s.my_tactics import MyTactics
from player2024s.predict_role import Predictions
import concurrent.futures

from player2024s.functions.generate_statement import generate_statement

from player2024s.info_types import GameInfo, GameSetting, TalkHistory
from typing import Union

from player2024s.dev_functions.log import clear_log, log, log_talk

class Agent2024s(Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        super().__init__(inifile, name)

        # ゲーム状況
        self.day: int = 0

        # 考察Class
        self.my_tactics = None
        self.stances = []
        self.predictions = None
        self.talkHistory = TalkHistory([])

    def get_info(self):
        data = json.loads(self.received.pop(0))

        self.gameInfo: Union[None, GameInfo] = data["gameInfo"] 
        self.gameSetting: Union[None, GameSetting] = data["gameSetting"]
        self.request = data["request"]
        if data["talkHistory"] is not None:
            self.talkHistory: TalkHistory = TalkHistory(data["talkHistory"])
        self.whisperHistory = data["whisperHistory"]
    
    def initialize(self):
        """
        initializeを受け取ったタイミングで実行されるmethod
        """
        super().initialize()
        # 考察Classの初期化
        self.init_stances()
        self.init_predictions()
        self.init_tacitcs()

        clear_log(self.index) # ログの初期化
    
    def daily_initialize(self) -> None:
        self.alive = []
        for agent_num, stance in enumerate(self.stances):
            if self.gameInfo["statusMap"][str(agent_num+1)] == "ALIVE":
                self.alive.append(agent_num+1)
                stance.update_alive(True)
            else:
                stance.update_alive(False)
        
        self.predictions.update_alive(self.alive)
        day:int = int(self.gameInfo["day"])
        self.day = day
    
    def talk(self) -> str:
        if self.day == 0:
            return "Over"
        
        # 他人のスタンスの更新
        self.update_stances()
        # 他人の予想役職の更新
        self.update_predictions()
        # 自分の戦略の更新
        self.update_my_tactics()
        # 発言（改行は含めない）
        statement = self.generate_statement().replace("\n", " ")
        self.save_talk_log(statement)
        return statement

    def save_talk_log(self, statement: str):
        msg=f"""
-----TALK-----
--update stances--
{"\n".join([f"{stance.target_agent_id} - {stance.day_stances}" for stance in self.stances])}

--update predictions--
{"\n".join([f"{predict_role.agent_id} - {predict_role.role} - {predict_role.reason}" for predict_role in self.predictions.predict_roles])}

--update my_tactics--
{self.my_tactics.tactics}

--statement--
{statement}
--------------
"""
        log(self.index, [msg])
        log_talk(self.index, self.role, statement)
    
    def vote(self) -> str:
        target_id = self.decide_vote()
        self.save_vote_log(target_id)

        data = {"agentIdx": target_id}
        return json.dumps(data, separators=(",",":"))

    def save_vote_log(self, target_id:int):
        log(self.index,[f"投票先を決定: 自分のid: {self.index}, target: {target_id}"])

    def update_stances(self):
        # スレッドプールエグゼキュータを使用して並列に処理
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # 各スタンスの更新タスクをサブミット
            futures = [executor.submit(stance.update, self.day, self.talkHistory) for stance in self.stances]
            # 全てのタスクが完了するのを待つ
            concurrent.futures.wait(futures)
    
    def update_predictions(self):
        self.predictions.update(self.stances)

    def update_my_tactics(self):
        self.my_tactics.update(self.day, self.stances, self.predictions)

    def generate_statement(self):
        return generate_statement(f"{int(self.index):02d}", self.role, self.talkHistory, self.my_tactics)

    def decide_vote(self) -> int:
        return self.my_tactics.decide_vote_target(self.index, self.role, self.alive)

    def init_stances(self):
        """
        initializeを受け取ったタイミングで実行
        """
        statusMap = self.gameInfo["statusMap"]
        self.stances = [Stance(f"{int(self.index):02d}", self.role, f"{int(agentId):02d}") for agentId in statusMap.keys()]

    def init_predictions(self):
        """
        initializeを受け取ったタイミングで実行
        """
        statusMap = self.gameInfo["statusMap"]
        self.predictions = Predictions(f"{int(self.index):02d}", self.role, self.gameSetting["roleNumMap"] ,statusMap)
    
    def init_tacitcs(self):
        """
        initializeを受け取ったタイミングで実行
        """
        self.my_tactics = MyTactics(f"{int(self.index):02d}", self.role, self.gameSetting["roleNumMap"])
    
    def hand_over(self, new_agent) -> None:
        super().hand_over(new_agent)
        new_agent.my_tactics = self.my_tactics
        new_agent.stances  = self.stances 
        new_agent.predictions = self.predictions
        new_agent.day = self.day