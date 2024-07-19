from player2024s.info_types import TalkHistory, GameInfo
from player2024s.functions.get_stance import get_stance


class Stance():
    """
    他プレイヤーのスタンス
    """
    def __init__(self, my_agent_id: str, my_agent_role: str, target_agent_id: str) -> None:
        # 基本情報
        self.target_agent_id: str = target_agent_id
        self.my_agent_id: str = my_agent_id
        self.my_agent_role: str = my_agent_role
        self.alive: bool = True
        # 考察
        self.day_stances: dict[int, str] = {} # 日毎の発言のまとめ
        # self.habit = None

    def update_alive(self, alive: bool) -> None:
        self.alive = alive
    
    def update(self, day:int, talk_history: TalkHistory):
        if not self.alive: return
        # 最初の発言の場合はupdate不要
        if len(talk_history) == 0: return

        stance:str = get_stance(self.my_agent_id, self.my_agent_role, self.target_agent_id, self.day_stances, talk_history)

        self.day_stances[day-1] = stance # 同じ日のスタンスは上書き