import asyncio

from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec

def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a * b


def add(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a + b
finance_tools = YahooFinanceToolSpec().to_tool_list()
# Add the custom functions to the tool list
finance_tools.extend([multiply, add])


workflow = FunctionAgent(
    name="Agent",
    description="Useful for performing financial operations.",
    llm=OpenAI(model="gpt-4o-mini"),
    tools=finance_tools,
    system_prompt="You are a helpful assistant.",
)


async def main():
    response = await workflow.run(
        user_msg="What's the current stock price of NVIDIA?"
    )
    print(response)

if __name__ == "__main__":
    asyncio.run(main())