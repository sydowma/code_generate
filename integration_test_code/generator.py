from langchain.chains.llm import LLMChain
from langchain.chains.sequential import SequentialChain
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate


class TestGenerator:
    def __init__(self):
        # 保持对话上下文，记住之前的测试生成逻辑
        self.memory = ConversationBufferMemory()
        # 或使用总结记忆，处理长对话
        self.summary_memory = ConversationSummaryMemory()
        self.llm = ChatOpenAI(temperature=0.1)
        self.memory = ConversationBufferMemory()
        self.code_analysis_prompt = self.create_code_analysis_prompt()
        self.test_design_prompt = self.create_test_design_prompt()
        self.code_generation_prompt = self.create_code_generation_prompt()

    def create_test_chain(self):
        # 1. 代码分析链
        analyze_chain = LLMChain(
            llm=self.llm,
            prompt=self.code_analysis_prompt
        )

        # 2. 测试设计链
        design_chain = LLMChain(
            llm=self.llm,
            prompt=self.test_design_prompt
        )

        # 3. 代码生成链
        generate_chain = LLMChain(
            llm=self.llm,
            prompt=self.code_generation_prompt
        )

        # 串联所有处理步骤
        return SequentialChain(
            chains=[analyze_chain, design_chain, generate_chain],
            input_variables=["code", "requirements"]
        )

    def create_code_analysis_prompt(self):
        return PromptTemplate(
            template="""
            Analyze the following code:
            {code}
            """,
            input_variables=["code"]
        )

    