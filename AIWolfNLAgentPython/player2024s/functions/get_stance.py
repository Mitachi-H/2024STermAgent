from player2024s.info_types import TalkHistory
from player2024s.langchain import OpenAIAgent

openai_agent = OpenAIAgent(temperature=1)

def get_stance(
        my_agent_id: str,
        my_agent_role: str,
        target_agent_id: str,
        day_stances: dict[int, str],
        talk_history: TalkHistory) -> str:
    """
    他のエージェントのスタンスをまとめる

    Args:
        my_agent_id (str): 自分のエージェントID
        my_agent_role (str): 自分の役職
        target_agent_id (str): 対象のエージェントID
        day_stances (dict[int, str]): 日毎のスタンス
        talk_history (TalkHistory): 発言履歴
    
    Returns:
        str: その日の、この関数を呼び出した時点での対象エージェントのスタンス
    """
    
    system = """
あなたはAgent[{my_agent_id}]という名前で人狼ゲームをプレイしています。
あなたの役職は{my_agent_role}です。
"""

    template = """
# 指示
このプロンプトでは、人狼ゲームにおける特定のエージェント（Agent[{target_agent_id}]）の発言と行動から情報を抽出し、そのエージェントのスタンスを評価します。対象エージェントの行動、役職推測、同意・非同意の表明などから、そのエージェントの意図や戦略を理解し、自エージェントの戦略に反映させる必要があります。

# 注意点
Agent[{target_agent_id}]がまだ発言していない場合、まとめは行わないでください。その場合出力は空欄としてください。

# タスク
1. 対象エージェントAgent[{target_agent_id}]が他のエージェントの役職についてどのように推測または宣言しているかを報告してください。
2. 対象エージェントAgent[{target_agent_id}]の最近の同意または非同意の行動を確認し、その基になる理由を考察してください。

# 出力形式
- 出力は以下の形式で整理してください：
  - 同意または非同意の行動: ...
  - 戦略予測: ...

# データ
- 発言履歴
{talk_history}
"""

    try:
        input = {"my_agent_id": my_agent_id, "my_agent_role": my_agent_role, "target_agent_id": target_agent_id, "day_stances": get_str_day_stances(day_stances), "talk_history": get_str_talk_history(talk_history)}

        output = openai_agent.chat(system, template, input)

        return output
    except Exception as e:
        print("error:", e)
        return ""

def get_str_day_stances(day_stances: dict[int, str]) -> str:
    return str(day_stances)

def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: f-stringで書きたいが、[]をエスケープする必要があるため、+演算子で結合
    return "\n".join(["Agent[0" + str(talk["agent"]) + "]\n" + talk["text"] for talk in talk_history])
