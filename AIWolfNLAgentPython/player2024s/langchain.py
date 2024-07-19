# """
# https://zenn.dev/umi_mori/books/prompt-engineer/viewer/langchain_overview
# """
from typing import List
from dotenv import load_dotenv
load_dotenv()
import os
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Type, Literal

from langchain_core.runnables.utils import Input
from typing import Literal

class OpenAIAgent():
    def __init__(self, model_name = "gpt-4o-mini", temperature = 0) -> None:
        # OpenAIのモデルのインスタンスを作成
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.json_llm = self.llm.bind(response_format={"type": "json_object"})
    
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

    def json_mode_chat(self, system: str, template: Literal["f-string", "mustache"], input: Input, pydantic_object: Type[BaseModel]) -> dict:
        output_parser = PydanticOutputParser(pydantic_object=pydantic_object)

        # Prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "{system}\nAnswer the user query. Wrap the output in `json` tags\n{format_instructions}",
                ),
                ("human", "{template}"),
            ]
        ).partial(format_instructions=output_parser.get_format_instructions())

        # OpenAIのAPIにこのプロンプトを送信するためのチェーンを作成
        chain = prompt | self.json_llm | output_parser

        return chain.invoke({"system": system, "template": template, **input})

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