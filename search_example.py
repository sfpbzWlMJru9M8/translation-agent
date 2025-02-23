from tools.vector_searcher import VectorSearcher

# 初始化查询器
searcher = VectorSearcher(persist_dir="./document_db")

# 列出所有可用的集合
available_collections = searcher.list_collections()
print("可用的集合:", available_collections)

# 在指定集合中搜索
query = "Starscourge Radahn"
results = searcher.search(
    query=query,
    collection_names=["translations",],  # 可以指定多个集合
    top_k=3,  # 每个集合返回前3个最相似的结果
    threshold=0.5  # 只返回相似度大于0.5的结果
)

# 打印搜索结果
for collection_name, collection_results in results.items():
    print(f"\n集合 '{collection_name}' 的搜索结果:")
    for i, result in enumerate(collection_results, 1):
        print(f"\n结果 {i}:")
        print(f"内容: {result['content'][:200]}...")  # 只显示前200个字符
        print(f"相似度: {result['similarity']:.2f}")
        if result['metadata']:
            print(f"元数据: {result['metadata']}") 