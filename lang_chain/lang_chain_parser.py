import json
import os

from langchain_community.adapters import openai
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_and_embed_documents():
    loader = GenericLoader.from_filesystem(
        "",
        glob="**/*",
        suffixes=[".java"],
        parser=LanguageParser("java")
    )
    docs = loader.load()

    embeddings = HuggingFaceEmbeddings(
        model_name="Kwaipilot/OASIS-code-embedding-1.5B"
    )

    if os.path.exists("faiss_index"):
        print("Loading faiss index")
        vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        return vector_store, embeddings
    embedded_docs = []
    for doc in docs:
        embedding_vector = embeddings.embed_query(doc.page_content)
        embedded_docs.append({
            'content': doc.page_content,
            'embedding': embedding_vector,
            'metadata': doc.metadata
        })

    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local("faiss_index")
    return vector_store, embeddings

def search_and_summarize(vector_store, embeddings, query="summarize the codebase", top_k=100):
    # 将查询转换为 embedding 并搜索
    query_embedding = embeddings.embed_query(query)
    results = vector_store.similarity_search_by_vector(query_embedding, k=top_k)

    # 提取目录结构和关键文件
    directory_structure = {}
    key_files = []

    for doc in results:
        # 从 metadata 中获取文件路径
        file_path = doc.metadata.get("source", "unknown")
        content_snippet = doc.page_content[:50]  # 取前200字符作为预览

        # 构建目录结构
        path_parts = file_path.split(os.sep)
        current_level = directory_structure
        for part in path_parts[:-1]:  # 排除文件名，只处理目录
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

        # 添加关键文件信息
        key_files.append({
            "file_path": file_path,
            "content_snippet": content_snippet,
            "similarity_score": doc.metadata.get("score", 1.0)  # FAISS 默认不返回分数，除非特别配置
        })

    # 返回结果
    summary = {
        "directory_structure": directory_structure,
        "key_files": key_files
    }
    return summary

def save_summary_to_json(summary, filename="codebase_summary.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    # 加载和嵌入文档
    print("Loading and embedding documents...")
    vector_store, embeddings = load_and_embed_documents()
    print("Loaded and embedded documents.")

    # 执行查询并生成 summary
    summary = search_and_summarize(vector_store, embeddings, query="summarize the codebase")

    # 打印结果
    print("Directory Structure:")
    print(json.dumps(summary["directory_structure"], indent=2))
    print("\nKey Files:")
    for file in summary["key_files"]:
        print(f"- {file['file_path']}: {file['content_snippet']}")

    # 保存到 JSON 文件
    save_summary_to_json(summary)

    # call openai api to generate a summary
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Please summarize the following codebase: {summary}"}
        ]
    )
    print(response)