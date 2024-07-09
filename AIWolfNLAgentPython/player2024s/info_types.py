from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Talk(BaseModel):
    agent: int
    day: int
    idx: int
    text: str
    turn: int

# TalkHistoryをList[Talk]として定義
class TalkHistory(List[Talk]):
    """
    その日のそれまでの会話のリスト。
    """

class PredictionRole(BaseModel):
    agent_id: str
    alive: bool
    role: Optional[str] = Field(default=None)
    reason: Optional[str] = Field(default=None)

class PredictionRoleList(BaseModel):
    content: List[PredictionRole]

class GameInfo(BaseModel):
    agent: int
    attackVoteList: List[int]
    attackedAgent: int
    cursedFox: int
    day: int
    divineResult: Optional[str] = None
    englishTalkList: List[Dict[str, str]]
    executedAgent: int
    existingRoleList: List[str]
    guardedAgent: int
    lastDeadAgentList: List[int]
    latestAttackVoteList: List[int]
    latestExecutedAgent: int
    latestVoteList: List[int]
    mediumResult: Optional[str] = None
    remainTalkMap: Dict[str, int]
    remainWhisperMap: Dict[str, int]
    roleMap: Dict[str, str]
    statusMap: Dict[str, str]
    talkList: List[Dict[str, str]]
    voteList: List[Dict[str, int]]
    whisperList: List[Dict[str, str]]