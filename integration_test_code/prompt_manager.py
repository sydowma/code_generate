from langchain.prompts import PromptTemplate


class TestPromptManager:
    def __init__(self):
        self.unit_test_prompt = PromptTemplate(
            template="""
            Based on the following:
            Code Context: {code_context}
            Dependencies: {dependencies}
            Test Requirements: {requirements}

            Generate a JUnit test that:
            1. Properly mocks all dependencies
            2. Covers all test cases
            3. Follows testing best practices
            """,
            input_variables=["code_context", "dependencies", "requirements"]
        )