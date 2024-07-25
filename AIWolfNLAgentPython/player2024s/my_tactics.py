from player2024s.stance import Stance
from player2024s.predict_role import Predictions
from player2024s.functions.get_tactic import get_tactic
from player2024s.functions.get_vote_target import get_vote_target
import random

class MyTactics():
    def __init__(self) -> None:
        self.tactics: list[str] = [] # 日毎の戦略
        pass

    def update(self,agent_id: int, day:int, stances: list[Stance], predictions: Predictions):
        tactic:str = get_tactic(agent_id, stances, predictions, self.tactics)

        if len(self.tactics) >= day: self.tactics.append("")
        self.tactics[day-1] = tactic # 同じ日のスタンスは上書きxw
    
    def decide_vote_target(self, agent_id: int, agent_role: str, alive: list[int]):
        for _ in range(5):
            target_id : int = get_vote_target(agent_id, agent_role, alive, self.tactics)

            # target_idが生きているか
            if target_id not in alive: continue

            # target_idが自分自身でないか
            if target_id == agent_id: continue

            return target_id
        return random.choice(alive)