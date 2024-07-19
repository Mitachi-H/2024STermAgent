from player2024s.stance import Stance
from player2024s.functions.get_prediction_role import get_prediction_role
from player2024s.info_types import PredictionRole, GameSetting
from typing import Dict


class Predictions():
    """
    自分から見た他プレイヤーの役職予想
    """
    def __init__(self, my_agent_id: str, my_agent_role: str, roleNumMap: Dict[str, int], statusMap) -> None:
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.roleNumMap: Dict[str, int] = roleNumMap
        self.predict_roles:list[PredictionRole] = [
            {"agent_id": agentId, "alive": True} for agentId in statusMap.keys()
        ]
        # self.reasons: str = None
    
    def update_alive(self, alive: list[int]):
        for predict_role in self.predict_roles:
            predict_role["alive"] = int(predict_role["agent_id"]) in alive
    
    def update(self, stances: list[Stance]):
        prediction_role: list[PredictionRole] = get_prediction_role(self.my_agent_id, self.my_agent_role, self.roleNumMap, stances, self.predict_roles)
        self.predict_roles = prediction_role
