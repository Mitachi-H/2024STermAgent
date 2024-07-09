from player2024s.info_types import PredictionRole
from player2024s.stance import Stance
from player2024s.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=x)

def get_tactic(
        agent_id: int,
        stances: list[Stance],
        predictions: list[PredictionRole],
        prev_tactics: list[str]
        ) -> str:
    """
    戦略の更新
    args:
    """

    system = "あなたは人狼ゲームをプレイしています"
    template = """
    あなたの名前はAgent[0{agent_id}]です。次にとるべき戦略を考えなさい。
    あなたの過去の戦略は以下のとおりです。
    {prev_tactics}
    ただし、これまでの発言のまとめは以下のとおりです。
    {stances}
    また各Agentの役職を推定結果は以下のとおりです。
    {predictions}
    """

    # input = {"agent_id": agent_id, "day_stances": get_str_day_stances(day_stances), "talk_history": get_str_talk_history(talk_history)}
    input = {"agent_id": agent_id, "stances": get_str_stances(stances), "predictions": get_str_predictions(predictions), "prev_tactics": get_str_prev_tactics(prev_tactics)}

    output = openai_agent.chat(system, template, input)
    # print(output)
    return output

# TODO: この関数を完成させる
def get_str_stances(stances: list[Stance]):
    return ""

def get_str_predictions(predict_roles: list[PredictionRole]) -> str:
    return " ".join([str(predictionRole) for predictionRole in predict_roles])

# TODO: この関数を完成させる
def get_str_prev_tactics(prev_tactics: list[str]):
    return ""
