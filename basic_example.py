#!/usr/bin/env python3
"""
Neo4j GraphRAG 基础示例
演示向量检索的基本用法
"""
import os
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import SentenceTransformerEmbeddings
from neo4j_graphrag.retrievers import VectorRetriever
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG

def setup_neo4j_data(driver):
    """创建示例数据"""
    print("创建示例数据...")

    with driver.session() as session:
        # 清除现有数据
        session.run("MATCH (n) DETACH DELETE n")

        # 创建向量索引
        session.run("""
            CREATE VECTOR INDEX document_embeddings IF NOT EXISTS
            FOR (d:Document)
            ON (d.embedding)
            OPTIONS {indexConfig: {
                `vector.dimensions`: 384,
                `vector.similarity_function`: 'cosine'
            }}
        """)

        # 示例文档数据
        documents = [
            {"id": 1, "content": "Neo4j是一个图数据库，专门用于存储和查询图结构数据", "title": "Neo4j简介"},
            {"id": 2, "content": "GraphRAG结合了图数据库和大语言模型，提供更准确的检索", "title": "GraphRAG概念"},
            {"id": 3, "content": "向量相似性搜索是RAG系统中的核心技术之一", "title": "向量搜索"},
            {"id": 4, "content": "知识图谱可以帮助AI系统更好地理解实体之间的关系", "title": "知识图谱"},
        ]

        # 创建文档节点
        for doc in documents:
            session.run("""
                CREATE (d:Document {
                    id: $id,
                    title: $title,
                    content: $content
                })
            """, id=doc["id"], title=doc["title"], content=doc["content"])

        print(f"✓ 创建了 {len(documents)} 个文档节点")

def add_embeddings(driver, embedder):
    """为文档添加嵌入向量"""
    print("生成嵌入向量...")

    with driver.session() as session:
        # 获取所有文档
        result = session.run("MATCH (d:Document) RETURN d.id as id, d.content as content")

        for record in result:
            doc_id = record["id"]
            content = record["content"]

            # 生成嵌入向量
            embedding = embedder.embed_query(content)

            # 更新文档的嵌入向量
            session.run("""
                MATCH (d:Document {id: $id})
                SET d.embedding = $embedding
            """, id=doc_id, embedding=embedding)

        print("✓ 已为所有文档添加嵌入向量")

def test_vector_retrieval(driver):
    """测试向量检索"""
    print("\n测试向量检索...")

    from neo4j_graphrag.retrievers import VectorRetriever

    # 创建检索器
    retriever = VectorRetriever(
        driver,
        index_name="document_embeddings",
        embedder=SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2")
    )

    # 测试查询
    queries = [
        "什么是图数据库？",
        "如何提高AI的回答准确性？",
        "什么是向量搜索？"
    ]

    for query in queries:
        print(f"\n查询: {query}")
        try:
            results = retriever.search(query_text=query, top_k=2)
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']}: {result['content'][:50]}...")
        except Exception as e:
            print(f"  ❌ 检索失败: {e}")

def test_with_openai(driver):
    """测试与OpenAI的集成"""
    print("\n=== 测试 OpenAI 集成 ===")

    # 检查是否设置了API密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  未设置 OPENAI_API_KEY，跳过 OpenAI 测试")
        print("请设置: export OPENAI_API_KEY='your-api-key'")
        return

    try:
        from neo4j_graphrag.llm import OpenAILLM
        from neo4j_graphrag.generation import GraphRAG

        # 创建LLM和检索器
        llm = OpenAILLM(model_name="gpt-3.5-turbo", model_params={"temperature": 0.1})
        retriever = VectorRetriever(
            driver,
            index_name="document_embeddings",
            embedder=SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2")
        )

        # 创建GraphRAG实例
        rag = GraphRAG(retriever=retriever, llm=llm)

        # 测试问答
        question = "什么是Neo4j？它有什么特点？"
        print(f"\n问题: {question}")

        response = rag.search(query_text=question, retriever_config={"top_k": 2})
        print(f"回答: {response.answer}")

    except Exception as e:
        print(f"❌ OpenAI 测试失败: {e}")

def main():
    """主函数"""
    print("=== Neo4j GraphRAG 基础示例 ===\n")

    # Neo4j连接配置
    URI = "neo4j://localhost:7687"
    AUTH = ("neo4j", "password")

    try:
        # 连接Neo4j
        print(f"连接到 Neo4j: {URI}")
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        print("✓ Neo4j 连接成功")

        # 创建嵌入器
        embedder = SentenceTransformerEmbeddings(model="all-MiniLM-L6-v2")
        print("✓ 嵌入器初始化成功")

        # 设置示例数据
        setup_neo4j_data(driver)

        # 添加嵌入向量
        add_embeddings(driver, embedder)

        # 测试向量检索
        test_vector_retrieval(driver)

        # 测试OpenAI集成
        test_with_openai(driver)

        print("\n🎉 示例运行成功！")

    except Exception as e:
        print(f"❌ 运行失败: {e}")
        print("请确保:")
        print("1. Neo4j 容器正在运行: docker ps | grep neo4j")
        print("2. 连接信息正确: URI='neo4j://localhost:7687', AUTH=('neo4j', 'password')")

    finally:
        if 'driver' in locals():
            driver.close()
            print("\n✓ 数据库连接已关闭")

if __name__ == "__main__":
    main()