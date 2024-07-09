from player2024s.info_types import PredictionRole, PredictionRoleList
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
    system = """
    あなたは人狼ゲームをプレイしています。
    ```
    """
    # TODO: 出力に必ずすべてのagentを含めるようにする
    template = """
    あなたの名前はAgent[0{agent_id}]です。stancesを参照して、各Agentの役職を推定しなさい。
    stances
    {stances}
    (参考): 過去の推定
    {prev_predict_roles}
    """

    input = {
        "stances": get_str_stances(stances),
        "prev_predict_roles": get_str_prev_predict_roles(prev_predict_roles)
    }

    output: PredictionRoleList = openai_agent.json_mode_chat(system, template, input, pydantic_object=PredictionRoleList)
    # print(output)
    # print("\n")
    return output

def get_str_stance(stance: Stance) -> str:
    return str(stance.day_stances)

def get_str_stances(stances: list[Stance]) -> str:
    return " ".join([get_str_stance(stance) for stance in stances])

def get_str_prev_predict_roles(prev_predict_roles: list[PredictionRole]) -> str:
    return " ".join([str(predictionRole) for predictionRole in prev_predict_roles])
