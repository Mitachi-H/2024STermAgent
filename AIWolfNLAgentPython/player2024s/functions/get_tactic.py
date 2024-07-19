from player2024s.predict_role import Predictions
from player2024s.info_types import PredictionRole
from player2024s.stance import Stance
from player2024s.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_tactic(
        agent_id: int,
        stances: list[Stance],
        predictions: Predictions,
        prev_tactics: list[str]
        ) -> str:
    """
    戦略の更新
    args:
        - agent_id: 自分のエージェントID
        - stances: 各エージェントのスタンス(5人分)
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

    input = {"agent_id": agent_id, "stances": get_str_stances(stances), "predictions": get_str_predictions(predictions), "prev_tactics": get_str_prev_tactics(prev_tactics)}

    output = openai_agent.chat(system, template, input)
    # print(output)
    return output

def get_str_stance(stance: Stance) -> str:
    return "Agent_id: " + stance.target_agent_id + "Stances: " +  str(stance.day_stances)

def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])

def get_str_predictions(predictions: Predictions) -> str:
    predict_roles:list[PredictionRole] = predictions.predict_roles
    return " ".join([str(predictionRole) for predictionRole in predict_roles])

# TODO: この関数を完成させる
def get_str_prev_tactics(prev_tactics: list[str]):
    return " ".join(prev_tactics)
