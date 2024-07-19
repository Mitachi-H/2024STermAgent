from player2024s.info_types import TalkHistory
from player2024s.langchain import OpenAIAgent
from player2024s.my_tactics import MyTactics

openai_agent = OpenAIAgent(temperature=1)

def generate_statement(
        talk_history: TalkHistory,
        my_tactics: MyTactics
        ) -> str:
    """
    実際の発言を出力
    """

    system = "あなたは人狼ゲームをプレイしています"
    template = """
    あなたの作戦は以下の通りです。（日にち毎に記録しており、最後の要素が最新です）
    {my_tactics}
    この作戦を元に、あなたの発言を示しなさい。ただし、発言のみを示すこと。
    また発言の内容は、いかに示す直前の会話から不自然のないものに努めること。
    {talk_history}
    """

    input = {"talk_history": get_str_talk_history(talk_history), "my_tactics": get_str_my_tactics(my_tactics)}

    output = openai_agent.chat(system, template, input)
    # print(output)
    return output

def get_str_my_tactics(my_tactics: MyTactics):
    my_day_tactics: list[str] = my_tactics.tactics
    return " ".join(my_day_tactics)

def get_str_talk_history(talk_history: TalkHistory) -> str:
    # MEMO: day, idx, turnはいらなそう
    return "".join([str(talk) for talk in talk_history])