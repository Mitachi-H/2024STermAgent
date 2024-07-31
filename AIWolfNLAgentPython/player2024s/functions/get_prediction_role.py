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
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
ゲームの参加者は全部で{num_agents}人です。
あなたの役職は{my_agent_role}です。
また、各役職の人数は以下の通りです。
{roleNumMap}
    """

    # TODO: 出力に必ずすべてのagentを含めるようにする
    # TODO: Divineの結果を含める。
    # TODO: 一貫性(自分の役職、Divineなら占いの結果との矛盾がないか)を確認する処理
    # 一人しか予想してくれない場合があった
    template = """
# 指示
このプロンプトでは、人狼ゲームにおける各エージェントの役職を予測することを目的としています。
予測はエージェントの発言のまとめと過去の役職推定を基に行います。この際、各役職の人数などの確定情報と矛盾がないか確認してください。
情報が不足している場合は、役職を特定できないことを示すためにroleと理由(reason)を「役職の予想に必要な情報が不足している」に設定してください。

# 注意点
- 複数の役職が考えられる場合は、それぞれの役職に対する確率を評価し、最も可能性が高い役職から順に記載します。
- 自分の役職は確定しているため、自分のエージェント(Agent[{my_agent_id}])については、roleは「{my_agent_role}」と、reasonは「自分の役職は確定している」と設定してください。

# 出力形式
以下のPredictionRoleList形式で出力してください。ただし出力は`json`タグで囲んでください。（PredictionRoleListはPredictionRoleのリストです。）
```
class PredictionRoleList(BaseModel):
    content: List[PredictionRole]

class PredictionRole(BaseModel):
    agent_id: int
    alive: bool
    role: Optional[str] = Field(default=None)
    reason: Optional[str] = Field(default=None)
```

# データ
- 各エージェントの発言のまとめ
{stances}
- 過去の役職推定
{prev_predict_roles}
"""

    input = {
        "my_agent_id": my_agent_id,
        "my_agent_role": my_agent_role,
        "roleNumMap": get_str_roleNumMap(roleNumMap),
        "stances": get_str_stances(stances),
        "prev_predict_roles": get_str_prev_predict_roles(prev_predict_roles),
        "num_agents": num_agents
    }

    output: PredictionRoleList = openai_agent.json_mode_chat(system, template, input, pydantic_object=PredictionRoleList)
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
    try:
        num_agents = sum(roleNumMap.values())
        system = """
    あなたはAgent[0{my_agent_id}]という名前で人狼ゲームをプレイしています。
    ゲームの参加者は全部で{num_agents}人です。
    あなたの役職は{my_agent_role}です。また、各役職の人数は以下の通りです。
    {roleNumMap}
        """

        template = """
# 指示
このプロンプトでは、人狼ゲームにおける各エージェントの役職を予測することを目的としています。
予測はエージェントの発言のまとめと過去の役職推定を基に行います。この際、各役職の人数や占い結果などの確定情報と矛盾がないか確認してください。
情報が不足している場合は、役職を特定できないことを示すためにroleと理由(reason)を「役職の予想に必要な情報が不足している」に設定してください。

# 注意点
- 複数の役職が考えられる場合は、それぞれの役職に対する確率を評価し、最も可能性が高い役職から順に記載します。
- 自分の役職は確定しているため、自分のエージェント(Agent[{my_agent_id}])については、roleは「{my_agent_role}」と、reasonは「自分の役職は確定している」と設定してください。

# 出力形式
以下のPredictionRoleList形式で出力してください。ただし出力は`json`タグで囲んでください。（PredictionRoleListはPredictionRoleのリストです。）
```
class PredictionRoleList(BaseModel):
    content: List[PredictionRole]

class PredictionRole(BaseModel):
    agent_id: int
    alive: bool
    role: Optional[str] = Field(default=None)
    reason: Optional[str] = Field(default=None)
```

# データ
- 占い結果
{divine_results}
- 各エージェントの発言のまとめ
{stances}
- 過去の役職推定
{prev_predict_roles}
"""

        input = {
            "my_agent_id": my_agent_id,
            "my_agent_role": my_agent_role,
            "roleNumMap": get_str_roleNumMap(roleNumMap),
            "stances": get_str_stances(stances),
            "prev_predict_roles": get_str_prev_predict_roles(prev_predict_roles),
            "num_agents": num_agents,
            "divine_results": get_str_divine_results(divine_results)
        }

        output: PredictionRoleList = openai_agent.json_mode_chat(system, template, input, pydantic_object=PredictionRoleList)
        result: list[PredictionRole] = output.content
        return result
    except Exception as e:
        print(e)
        return []

def get_str_roleNumMap(roleNumMap: Dict[str, int]) -> str:
    # MEMO: num > 0 のroleのみ表示
    return " ".join([f"{role}: {num}" for role, num in roleNumMap.items() if num > 0])

def get_str_stance(stance: Stance) -> str:
    return f"Agent_id:[{stance.target_agent_id}] - Stances: {str(stance.day_stances)}"

def get_str_stances(stances: list[Stance]) -> str:
    return "\n".join([get_str_stance(stance) for stance in stances])

def get_str_prev_predict_roles(prev_predict_roles: list[PredictionRole]) -> str:
    return " ".join([str(predictionRole) for predictionRole in prev_predict_roles])

def get_str_divine_results(divine_results: List[DivineResult]):
    return " ".join([str(divine_result) for divine_result in divine_results])
