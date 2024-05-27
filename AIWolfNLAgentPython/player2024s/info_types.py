from typing import List, Dict, Optional, TypedDict

class GameInfo(TypedDict):
    agent: int
    attackVoteList: List[int]
    attackedAgent: int
    cursedFox: int
    day: int
    divineResult: Optional[str]
    englishTalkList: List[Dict[str, str]]
    executedAgent: int
    existingRoleList: List[str]
    guardedAgent: int
    lastDeadAgentList: List[int]
    latestAttackVoteList: List[int]
    latestExecutedAgent: int
    latestVoteList: List[int]
    mediumResult: Optional[str]
    remainTalkMap: Dict[str, int]
    remainWhisperMap: Dict[str, int]
    roleMap: Dict[str, str]
    statusMap: Dict[str, str]
    talkList: List[Dict[str, str]]
    voteList: List[Dict[str, int]]
    whisperList: List[Dict[str, str]]

class Talk(TypedDict):
    agent: int
    day: int
    idx: int
    text: str
    turn: int

class TalkHistory(List[Talk]):
    pass