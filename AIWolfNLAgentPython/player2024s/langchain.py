# """
# https://zenn.dev/umi_mori/books/prompt-engineer/viewer/langchain_overview
# """

from dotenv import load_dotenv
load_dotenv()
import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from langchain_core.runnables.utils import Input
from typing import Literal

class OpenAIAgent():
    def __init__(self, model_name = "gpt-3.5-turbo", temperature = 0) -> None:
        # OpenAIのモデルのインスタンスを作成
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
    
    def chat(self, system: str, template: Literal["f-string", "mustache"], input: Input) -> str:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("user", template)
        ])
        # チャットメッセージを文字列に変換するための出力解析インスタンスを作成
        output_parser = StrOutputParser()

        # OpenAIのAPIにこのプロンプトを送信するためのチェーンを作成
        chain = prompt | self.llm | output_parser

        return chain.invoke(input)

    def test_chat(self):
        # プロンプトのテンプレート文章を定義
        template = """
        次の文章に誤字がないか調べて。誤字があれば訂正してください。
        {sentences_before_check}
        """

        # テンプレート文章にあるチェック対象の単語を変数化
        prompt = ChatPromptTemplate.from_messages([
            ("system", "あなたは優秀な校正者です。"),
            ("user", template)
        ])

        # チャットメッセージを文字列に変換するための出力解析インスタンスを作成
        output_parser = StrOutputParser()

        # OpenAIのAPIにこのプロンプトを送信するためのチェーンを作成
        chain = prompt | self.llm | output_parser

        # チェーンを実行し、結果を表示
        print(chain.invoke({"sentences_before_check": "こんんんちわ、真純です。"}))