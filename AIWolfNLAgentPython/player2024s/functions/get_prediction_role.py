from player2024s.info_types import PredictionRole, PredictionRoleList
from player2024s.stance import Stance
from player2024s.langchain import OpenAIAgent
from typing import Dict

openai_agent = OpenAIAgent(temperature=1)

def get_prediction_role(
        my_agent_id: str,
        my_agent_role: str,
        roleNumMap: Dict[str, int],
        stances: list[Stance],
        prev_predict_roles: list[PredictionRole]
        ) -> list[PredictionRole]:
    """
    予想役職の更新
    """
    num_agents = sum(roleNumMap.values())
    system = """
    あなたは人狼ゲームをプレイしています。
    ゲームの参加者は{num_agents}人です。また、各役職の人数は以下の通りです。
    {roleNumMap}
    ```
    """
    # TODO: 出力に必ずすべてのagentを含めるようにする
    # TODO: Divineの結果を含める。
    # TODO: 一貫性(自分の役職、Divineなら占いの結果との矛盾がないか)を確認する処理
    # 一人しか予想してくれない場合があった
    template = """
    あなたの名前はAgent[0{my_agent_id}]で、あなたの役職は{my_agent_role}です。
    stancesを参照して、「すべての」Agentについて、その役職を推定しなさい。
    stances
    {stances}
    (参考): 過去の推定
    {prev_predict_roles}
    """

    input = {
        "my_agent_id": my_agent_id,
        "my_agent_role": my_agent_role,
        "roleNumMap": roleNumMap,
        "stances": get_str_stances(stances),
        "prev_predict_roles": get_str_prev_predict_roles(prev_predict_roles),
        "num_agents": num_agents
    }

    output: PredictionRoleList = openai_agent.json_mode_chat(system, template, input, pydantic_object=PredictionRoleList)
    # print(output)
    # print("\n")
    return output

def get_str_stance(stance: Stance) -> str:
    return "Agent_id: " + stance.target_agent_id + "Stances: " +  str(stance.day_stances)

def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])

def get_str_prev_predict_roles(prev_predict_roles: list[PredictionRole]) -> str:
    return " ".join([str(predictionRole) for predictionRole in prev_predict_roles])
