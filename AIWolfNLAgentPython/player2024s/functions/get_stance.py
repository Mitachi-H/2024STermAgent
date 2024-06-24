from player2024s.info_types import TalkHistory
from player2024s.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_stance(agent_id: str, day_stances: list[str], talk_history: TalkHistory) -> str:
    """
    AgentのStanceの更新
    """
    system = "あなたは人狼ゲームをプレイしています"
    template = """
    あなたの名前はAgent[0{agent_id}]です。
    {talk_history}を参照して、あなたの発言をまとめなさい。
    ただし、これまでの発言のまとめは以下のとおりです。
    {day_stances}
    """

    input = {"agent_id": agent_id, "day_stances": get_str_day_stances(day_stances), "talk_history": get_str_talk_history(talk_history)}

    output = openai_agent.chat(system, template, input)
    print(output)
    return output

def get_str_day_stances(day_stances: list[str]) -> str:
    return " ".join(day_stances)

def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: day, idx, turnはいらなそう
    # TODO: strしてからjoinだと間違い。
    return " ".join(str(talk_history))
