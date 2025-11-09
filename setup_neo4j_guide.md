# Neo4j GraphRAG 安装指南

## ✅ 已完成
- Python 3.12.2 ✓
- Neo4j GraphRAG 包 ✓
- 依赖包安装 ✓

## 🔄 设置 Neo4j 数据库

您有以下几种选择来运行 Neo4j：

### 选项 1: Neo4j AuraDB (推荐 - 免费云端版本)
1. 访问 [Neo4j AuraDB](https://neo4j.com/cloud/aura-db/)
2. 注册免费账户
3. 创建免费数据库实例
4. 获取连接 URI 和密码

### 选项 2: 本地安装 Neo4j Desktop
```bash
# 下载 Neo4j Desktop
# 访问: https://neo4j.com/download/
```

### 选项 3: 使用 Docker (如果网络允许)
```bash
# 使用更小的镜像
docker run -d --name neo4j-community \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_dbms_security_procedures_unrestricted=apoc.* \
  -e NEO4J_dbms_security_procedures_allowlist=apoc.* \
  neo4j:4.4-community
```

### 选项 4: 使用现有图数据库服务
我看到您的环境中已经运行了 Dify 系统，它可能包含 Weaviate 服务。我们可以直接进行一些基础的 GraphRAG 概念演示。

## 🚀 快速开始 (使用 AuraDB)

如果您选择了 AuraDB，请按以下步骤：

1. **设置环境变量**
```bash
export NEO4J_URI="neo4j+s://xxxx.databases.neo4j.io"
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="your-password"
```

2. **运行测试脚本**
```bash
source graphrag_env/bin/activate
python test_installation.py
```

3. **运行基础示例**
```bash
source graphrag_env/bin/activate
python basic_example.py
```

## 📝 下一步

一旦 Neo4j 数据库设置完成，我们就可以开始：

1. **基础向量检索** - 演示文档相似性搜索
2. **知识图谱构建** - 从文本提取实体和关系
3. **混合检索** - 结合向量和图查询
4. **完整问答系统** - 构建实际应用

## 🔧 故障排除

如果遇到连接问题：
```bash
# 检查端口占用
netstat -an | grep 7687

# 测试连接
source graphrag_env/bin/activate
python test_installation.py
```

需要帮助？请告诉我您选择的设置方式！