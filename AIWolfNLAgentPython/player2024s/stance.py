class Stance():
    """
    他プレイヤーのスタンス
    """
    def __init__(self, agent_id: str) -> None:
        # 基本情報
        self.agent_id: str = agent_id
        self.alive: bool = True
        # 考察
        self.stance: list[str] = [] # 日毎の発言のまとめ
        # self.habit = None

    def update_alive(self, alive: bool) -> None:
        self.alive = alive