from player2024s.predict_role import Predictions
from player2024s.info_types import PredictionRole
from player2024s.stance import Stance
from player2024s.langchain import OpenAIAgent
from typing import Dict, List

openai_agent = OpenAIAgent(temperature=1)

def get_tactic(
        my_agent_id: str,
        my_agent_role: str,
        roleNumMap: Dict[str, int],
        stances: list[Stance],
        predictions: Predictions,
        prev_tactics: dict[int, str]
        ) -> str:
    """
    戦略の更新
    args:
        - agent_id: 自分のエージェントID
        - stances: 各エージェントのスタンス(5人分)
    """

    num_agents = sum(roleNumMap.values())

    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
ゲームの参加者は全部で{num_agents}人です。
あなたの役職は{my_agent_role}です。
また、各役職の人数は以下の通りです。
{roleNumMap}
"""

    template = """
# 指示
このプロンプトでは、あなたの現在のゲーム状況と他のエージェントとの相互作用を考慮して、効果的な戦略を生成することを目的としています。予測された役職や過去の戦略、現在のエージェントのスタンスを基に、次の行動計画を立ててください。

# タスク
1. 現在のゲーム状況を分析し、どのエージェントが最も影響力があるかを判断します。
2. 他のエージェントの役職推定とその根拠を考慮し、どのエージェントを支援または攻撃するかを決定します。
3. これまでの戦略と現在の状況を比較し、新たなアプローチを考案してください。

# 出力形式
- 出力は具体的な行動計画とその理由を含む形で整理してください。

# データ
- 各エージェントの発言のまとめ
{stances}
- 各エージェントの役職推定
{predictions}
- 過去の戦略
{prev_tactics}
"""

    try:
        input = {
            "my_agent_id": my_agent_id,
            "my_agent_role": my_agent_role,
            "roleNumMap": get_str_roleNumMap(roleNumMap),
            "stances": get_str_stances(stances),
            "predictions": get_str_predictions(predictions),
            "prev_tactics": get_str_prev_tactics(prev_tactics),
            "num_agents": num_agents
        }

        output = openai_agent.chat(system, template, input)
        return output
    except Exception as e:
        print(e)
        return ""

def get_str_roleNumMap(roleNumMap: Dict[str, int]) -> str:
    # MEMO: num > 0 のroleのみ表示
    return " ".join([f"{role}: {num}" for role, num in roleNumMap.items() if num > 0])

def get_str_stance(stance: Stance) -> str:
    return "Agent_id: " + stance.target_agent_id + "Stances: " +  str(stance.day_stances)

def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])

def get_str_predictions(predictions: Predictions) -> str:
    predict_roles:list[PredictionRole] = predictions.predict_roles
    return " ".join([str(predictionRole) for predictionRole in predict_roles])

def get_str_prev_tactics(prev_tactics: dict[int, str]):
    return " ".join([f"day: {day}, tactic: {tactic}" for day, tactic in prev_tactics.items()])
