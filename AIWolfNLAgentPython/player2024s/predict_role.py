from player2024s.stance import Stance
from player2024s.functions.get_prediction_role import get_prediction_role
from player2024s.info_types import PredictionRole


class Predictions():
    def __init__(self, statusMap) -> None:
        self.predict_roles:list[PredictionRole] = [
            {"agent_id": agentId, "alive": True} for agentId in statusMap.keys()
        ]
        # self.reasons: str = None
    
    def update_alive(self, alive: list[int]):
        for predict_role in self.predict_roles:
            predict_role["alive"] = int(predict_role["agent_id"]) in alive
    
    def update(self, stances: list[Stance]):
        prediction_role: list[PredictionRole] = get_prediction_role(stances, self.predict_roles)
        self.predict_roles = prediction_role
