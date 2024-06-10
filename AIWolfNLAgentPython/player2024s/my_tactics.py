from player2024s.stance import Stance
from player2024s.predict_role import Predictions
from player2024s.functions.get_tactic import get_tactic

class MyTactics():
    def __init__(self) -> None:
        self.tactics: list[str] = [] # 日毎の戦略
        pass

    def update(self, day:int, stances: list[Stance], predictions: Predictions):
        tactic:str = get_tactic(stances, predictions, self.tactics)

        if len(self.tactics) >= day: self.tactics.append("")
        self.tactics[day-1] = tactic # 同じ日のスタンスは上書きxw