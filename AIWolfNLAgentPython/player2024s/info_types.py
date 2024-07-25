from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

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

class DivineResult(BaseModel):
    agent: int
    day: int
    result: Literal["HUMAN", "WEREWOLF"]
    target: int

class GameInfo(BaseModel):
    agent: int
    attackVoteList: List[int]
    attackedAgent: int
    cursedFox: int
    day: int
    divineResult: Optional[DivineResult] = None
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

class GameSetting(BaseModel):
    enableNoAttack: bool
    enableNoExecution: bool
    enableRoleRequest: bool
    maxAttackRevote: int
    maxRevote: int
    maxSkip: int
    maxTalk: int
    maxTalkTurn: int
    maxWhisper: int
    maxWhisperTurn: int
    playerNum: int
    randomSeed: int
    roleNumMap: Dict[str, int]
    talkOnFirstDay: bool
    timeLimit: int
    validateUtterance: bool
    votableInFirstDay: bool
    voteVisible: bool
    whisperBeforeRevote: bool
