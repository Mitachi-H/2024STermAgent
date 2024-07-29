from player2024s.stance import Stance
from player2024s.functions.get_prediction_role import get_prediction_role, get_prediction_role_for_seer
from player2024s.info_types import PredictionRole, DivineResult
from typing import Dict, List, Optional


class Predictions():
    """
    自分から見た他プレイヤーの役職予想
    """
    def __init__(self, my_agent_id: str, my_agent_role: str, roleNumMap: Dict[str, int], statusMap) -> None:
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.roleNumMap: Dict[str, int] = roleNumMap
        self.predict_roles: list[PredictionRole] = [PredictionRole(agent_id=agent_id, alive=True) for agent_id in statusMap.keys()]
        # self.reasons: str = None
    
    def update_alive(self, alive: list[int]):
        print("--- Predict Role ---")
        for predict_role in self.predict_roles:
            print(predict_role)
            predict_role.alive = int(predict_role.agent_id) in alive
        print("------")
    
    def update(self, stances: list[Stance], divine_results: Optional[List[DivineResult]] = None):
        if divine_results is None:
            prediction_role: list[PredictionRole] = get_prediction_role(self.my_agent_id, self.my_agent_role, self.roleNumMap, stances, self.predict_roles)
        else:
            prediction_role: list[PredictionRole] = get_prediction_role_for_seer(self.my_agent_id, self.my_agent_role, self.roleNumMap, stances, self.predict_roles, divine_results)
        self.predict_roles = prediction_role
