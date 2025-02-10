from langchain.chains.llm import LLMChain
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


class TestGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.1)
        self.prompt = self._create_prompt()

    def _create_prompt(self):
        return PromptTemplate()

    def load_context(self, file_path):
        # 加载代码文件
        loader = TextLoader(file_path)
        documents = loader.load()

        # 分割代码以确保在上下文窗口内
        text_splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        return texts

    def generate_test(self, requirements, template, context_files):
        # 加载所有相关文件的上下文
        context = ""
        for file in context_files:
            context += self.load_context(file)

        # 生成测试代码
        chain = LLMChain(llm=self.llm, prompt=self.prompt)
        return chain.run({
            "requirements": requirements,
            "template": template,
            "context": context
        })


if __name__ == '__main__':
    # 1. 定义提示模板
    # test_prompt = PromptTemplate(
    #     input_variables=["requirements", "template", "context"],
    #     template="""
    #     Based on the following information, please generate a unit test:
    #
    #     Requirements:
    #     {requirements}
    #
    #     Template:
    #     {template}
    #
    #     Code Context:
    #     {context}
    #
    #     Please generate a complete unit test that follows the template structure and meets the requirements.
    #     """
    # )
    #
    # # 2. 设置 LLM
    # llm = ChatOpenAI(temperature=0.1)
    #
    # # 3. 创建链
    # chain = LLMChain(llm=llm, prompt=test_prompt)
    #
    # # 4. 运行生成
    # test_code = chain.run({
    #     "requirements": "your test requirements",
    #     "template": "your test template",
    #     "context": "your code context"
    # })
    # print(test_code)
    generator = TestGenerator()

    requirements = """
    Write a test case for the login function:
    1. Test successful login
    2. Test failed login with wrong password
    3. Test failed login with non-existent user
    """

    template = """
    def test_login():
        # Test setup

        # Test execution

        # Assertions
    """

    context_files = [
        "auth.py",
        "models/user.py"
    ]

    test_code = generator.generate_test(
        requirements=requirements,
        template=template,
        context_files=context_files
    )
    print(test_code)