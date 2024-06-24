from player2024s.info_types import PredictionRole
from player2024s.stance import Stance
from player2024s.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_prediction_role(
        stances: list[Stance],
        prev_predict_roles: list[PredictionRole]
        ) -> list[PredictionRole]:
    """
    予想役職の更新
    """
    system = "あなたは人狼ゲームをプレイしています"
    template = """
    あなたの名前はAgent[0{agent_id}]です。
    {talk_history}を参照して、あなたの発言をまとめなさい。
    ただし、これまでの発言のまとめは以下のとおりです。
    {day_stances}
    """

    input = {"stances": get_str_stances(stances), "prev_predict_roles": get_str_prev_predict_roles(prev_predict_roles)}

    output = openai_agent.chat(system, template, input)
    print(output)
    return []

def get_str_stance(stance: Stance) -> str:
    pass

def get_str_stances(day_stances: list[Stance]) -> str:
    stances = []
    # TODO: stancesをget_str_stanceを使って更新
    return " ".join(stances)

def get_str_prev_predict_roles(prev_predict_roles: list[PredictionRole]) -> str:
    # TODO: strしてからjoinだと間違い。
    return " ".join(str(prev_predict_roles))