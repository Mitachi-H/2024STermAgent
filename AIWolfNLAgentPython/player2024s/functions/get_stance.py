from player2024s.info_types import TalkHistory
from player2024s.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_stance(
        my_agent_id: str,
        my_agent_role: str,
        target_agent_id: str,
        day_stances: dict[int, str],
        talk_history: TalkHistory) -> str:
    """
    他のエージェントのスタンスをまとめる

    Args:
        my_agent_id (str): 自分のエージェントID
        my_agent_role (str): 自分の役職
        target_agent_id (str): 対象のエージェントID
        day_stances (dict[int, str]): 日毎のスタンス
        talk_history (TalkHistory): 発言履歴
    
    Returns:
        str: その日の、この関数を呼び出した時点での対象エージェントのスタンス
    """
    
    system = """
    あなたはAgent[0{my_agent_id}]という名前で人狼ゲームをプレイしています。
    あなたの役職は{my_agent_role}です。
    """

    template = """
    {talk_history}を参照して、Agent[0{target_agent_id}]の発言をまとめなさい。
    ただし、これまでの日毎の発言のまとめは以下のとおりです。
    {day_stances}
    """

    input = {"my_agent_id": my_agent_id, "my_agent_role": my_agent_role, "target_agent_id": target_agent_id, "day_stances": get_str_day_stances(day_stances), "talk_history": get_str_talk_history(talk_history)}

    output = openai_agent.chat(system, template, input)
    return output

def get_str_day_stances(day_stances: dict[int, str]) -> str:
    return str(day_stances)

def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: day, idx, turnはいらなそう
    return "".join([str(talk) for talk in talk_history])
