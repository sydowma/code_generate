import asyncio
from typing import List, Optional

from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.node_parser import CodeSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding


class CodeParser:
    """A class to handle code parsing and querying using LlamaIndex."""
    
    def __init__(
        self,
        input_dir: str = "spring-request",
        model_name: str = "BAAI/bge-large-en-v1.5",
        llm_model: str = "llama3.1:latest",
        # llm_model: str = "gpt-4o-mini",
        storage_path: str = "storage",
        language: str = "java"
    ):
        """Initialize the CodeParser with configuration parameters.
        
        Args:
            input_dir: Directory containing code files to parse
            model_name: Name of the embedding model to use
            llm_model: Name of the LLM model to use
            storage_path: Path to store the index
            language: Programming language of the code files
        """
        self.input_dir = input_dir
        self.storage_path = storage_path
        
        # Configure settings
        self._setup_settings(model_name, llm_model, language)
        
        # Initialize components
        self.index = self._create_index()
        self.query_engine = self._create_query_engine()
        self.agent = self._create_agent()

    def _setup_settings(self, model_name: str, llm_model: str, language: str) -> None:
        """Configure LlamaIndex settings."""
        code_splitter = CodeSplitter(language=language)
        Settings.code_splitter = code_splitter
        Settings.embed_model = HuggingFaceEmbedding(model_name=model_name)
        # Settings.embed_model = OpenAIEmbedding(embed_batch_size=42)
        Settings.llm = Ollama(model=llm_model, request_timeout=360.0)
        # Settings.llm = OpenAI(model=llm_model)

    def _create_index(self) -> VectorStoreIndex:
        """Create and persist the vector store index."""
        documents = SimpleDirectoryReader(
            input_dir=self.input_dir,
            required_exts=['.java'],
            recursive=True
        ).load_data()
        
        index = VectorStoreIndex.from_documents(
            documents,
            transformations=[Settings.code_splitter]
        )
        index.storage_context.persist(self.storage_path)
        return index

    def _create_query_engine(self):
        """Create the query engine."""
        return self.index.as_query_engine(llm=Settings.llm)

    def _create_agent(self) -> AgentWorkflow:
        """Create the agent workflow."""
        return AgentWorkflow.from_tools_or_functions(
            [self.search_documents],
            llm=Settings.llm,
            system_prompt="""You are a helpful assistant that can perform calculations
            and search through documents to answer questions."""
        )

    async def search_documents(self, query: str) -> str:
        """Search through documents using the query engine.
        
        Args:
            query: The search query string
            
        Returns:
            str: The response from the query engine
        """
        response = await self.query_engine.aquery(query)
        return str(response)

    async def analyze_repository(self) -> str:
        """Analyze the repository and provide a detailed summary.
        
        Returns:
            str: A detailed summary of the repository
        """
        return await self.agent.run(
            """Please analyze this code repository and provide a comprehensive summary that includes:
            1. Overall project structure and architecture
            2. Main components and their purposes
            3. Key functionalities and features
            4. Dependencies and technologies used
            5. Notable patterns or design decisions
            6. Potential areas for improvement
            
            Please organize the information in a clear, structured manner."""
        )


async def main():
    """Main function to demonstrate the CodeParser usage."""
    parser = CodeParser(input_dir='/Users/oker/GitHub/download/project-x/src')
    response = await parser.analyze_repository()
    print(response)


if __name__ == "__main__":
    asyncio.run(main())

