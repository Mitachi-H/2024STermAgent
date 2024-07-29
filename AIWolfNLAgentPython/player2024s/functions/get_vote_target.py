from player2024s.langchain import OpenAIAgent
from pydantic import BaseModel

class VoteTarget(BaseModel):
    target_id: int


openai_agent = OpenAIAgent(temperature=1)

def get_vote_target(
        agent_id: int,
        role: str,
        alive: list[int],
        my_tactics: list[str]
    ) -> int:
    """
    投票先の決定

    Args:
        agent_id: 自分のエージェントID
        alive: 生存者リスト
        my_tactics: 自分の日毎の戦略のリスト
    """

    system = "あなたは人狼ゲームをプレイしています"
    template = """
    あなたの名前はAgent[0{agent_id}]です。あなたの役職は{role}です。
    このゲームに勝利するために今日どのエージェントを処刑するべきか、エージェントのidをintで指定してください。
    投票数が最も多かったエージェントは処刑されます。

    生存者のidは以下の通りです。
    {alive}
    あなたの日毎の戦略は以下のとおりです。
    {my_tactics}
    """

    input = {"agent_id": agent_id, "role": role, "alive": alive, "my_tactics": my_tactics}

    output: VoteTarget = openai_agent.json_mode_chat(system, template, input, pydantic_object=VoteTarget)

    print("--- Vote Target ---")
    print(output)
    print(input)
    print("------")
    return output.target_id