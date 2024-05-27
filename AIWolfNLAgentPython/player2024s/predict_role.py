class PredictRole():
    def __init__(self, agent_id: str) -> None:
        # 基本情報
        self.agent_id: str = agent_id
        self.alive: bool = True
        # 考察
        self.role: str = None
        self.reason = None
    
    def update_alive(self, alive: bool) -> None:
        self.alive = alive