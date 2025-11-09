#!/usr/bin/env python3
"""
测试 Neo4j GraphRAG 安装是否成功
"""
import sys

def test_imports():
    """测试所有必要的包是否可以导入"""
    try:
        print("测试包导入...")

        # 测试基础包
        import neo4j
        print("✓ neo4j")

        import neo4j_graphrag
        print("✓ neo4j_graphrag")

        # 测试嵌入模型
        from neo4j_graphrag.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings
        print("✓ embeddings")

        # 测试检索器
        from neo4j_graphrag.retrievers import VectorRetriever, HybridRetriever
        print("✓ retrievers")

        # 测试 LLM
        from neo4j_graphrag.llm import OpenAILLM
        print("✓ llm")

        # 测试其他包
        import sentence_transformers
        print("✓ sentence_transformers")

        import openai
        print("✓ openai")

        print("\n🎉 所有包导入成功！")
        return True

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_neo4j_connection():
    """测试 Neo4j 连接"""
    try:
        from neo4j import GraphDatabase

        # 连接配置
        URI = "neo4j://localhost:7687"
        AUTH = ("neo4j", "password")

        print(f"\n测试连接到 Neo4j: {URI}")
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        print("✓ Neo4j 连接成功！")

        # 简单查询测试
        with driver.session() as session:
            result = session.run("RETURN 'Hello Neo4j!' as message")
            record = result.single()
            print(f"✓ 查询测试成功: {record['message']}")

        driver.close()
        return True

    except Exception as e:
        print(f"❌ Neo4j 连接失败: {e}")
        print("请确保 Neo4j 容器正在运行")
        return False

if __name__ == "__main__":
    print("=== Neo4j GraphRAG 安装测试 ===\n")

    # 测试包导入
    if not test_imports():
        sys.exit(1)

    # 测试 Neo4j 连接
    test_neo4j_connection()

    print("\n=== 测试完成 ===")
    print("\n下一步:")
    print("1. 设置 OpenAI API Key: export OPENAI_API_KEY='your-api-key'")
    print("2. 运行基础示例: python basic_example.py")