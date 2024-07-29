from player2024s.info_types import PredictionRole, PredictionRoleList
from player2024s.stance import Stance
from player2024s.langchain import OpenAIAgent
from player2024s.info_types import PredictionRole, DivineResult
from typing import Dict, List

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
    あなたはAgent[0{my_agent_id}]という名前で人狼ゲームをプレイしています。
    ゲームの参加者は全部で{num_agents}人です。
    あなたの役職は{my_agent_role}です。また、各役職の人数は以下の通りです。
    {roleNumMap}
    """

    # TODO: 出力に必ずすべてのagentを含めるようにする
    # TODO: Divineの結果を含める。
    # TODO: 一貫性(自分の役職、Divineなら占いの結果との矛盾がないか)を確認する処理
    # 一人しか予想してくれない場合があった
    template = """
    stances(各Agentの日中の発言のまとめ)を参照して、「すべての」Agentについて、その役職を具体的に推定しなさい。またその際、推定の根拠を簡潔かつ論理的に述べること。
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
    result: list[PredictionRole] = output.content
    return result

def get_prediction_role_for_seer(
        my_agent_id: str,
        my_agent_role: str,
        roleNumMap: Dict[str, int],
        stances: list[Stance],
        prev_predict_roles: list[PredictionRole],
        divine_results: List[DivineResult]
        ) -> list[PredictionRole]:
    """
    占い師用の予想役職の更新。占い結果もプロンプトに含める
    """
    num_agents = sum(roleNumMap.values())
    system = """
    あなたはAgent[0{my_agent_id}]という名前で人狼ゲームをプレイしています。
    ゲームの参加者は全部で{num_agents}人です。
    あなたの役職は{my_agent_role}です。また、各役職の人数は以下の通りです。
    {roleNumMap}
    """
    # TODO: 出力に必ずすべてのagentを含めるようにする
    # TODO: Divineの結果を含める。
    # TODO: 一貫性(自分の役職、Divineなら占いの結果との矛盾がないか)を確認する処理
    # 一人しか予想してくれない場合があった
    template = """
    divine_resultsとstances(各Agentの日中の発言のまとめ)を参照して、「すべての」Agentについて、その役職を具体的に推定しなさい。またその際、推定の根拠を簡潔かつ論理的に述べること。
    ただし推定を行う際、divine_resultsの結果を中心に、その結果に矛盾しないように注意すること。
    divine_results
    {divine_results}
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
        "num_agents": num_agents,
        "divine_results": get_str_divine_results(divine_results)
    }

    output: PredictionRoleList = openai_agent.json_mode_chat(system, template, input, pydantic_object=PredictionRoleList)
    # print(output)
    # print("\n")
    result: list[PredictionRole] = output.content
    return result


def get_str_stance(stance: Stance) -> str:
    return "Agent_id: " + stance.target_agent_id + "Stances: " +  str(stance.day_stances)

def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])

def get_str_prev_predict_roles(prev_predict_roles: list[PredictionRole]) -> str:
    return " ".join([str(predictionRole) for predictionRole in prev_predict_roles])

def get_str_divine_results(divine_results: List[DivineResult]):
    return " ".join([str(divine_result) for divine_result in divine_results])
