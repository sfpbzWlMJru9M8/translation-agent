from tools.file_processor import FileProcessor
import logging
import os

# 设置日志级别
logging.basicConfig(level=logging.INFO)

# 确保目录存在
os.makedirs("./document_db", exist_ok=True)
os.makedirs("./documents", exist_ok=True)

# 初始化处理器
processor = FileProcessor(
    persist_dir="./document_db",
    collection_name="translations",
    chunk_size=500,  # 调整分块大小
    chunk_overlap=50  # 调整重叠大小
)

# 处理文件
try:
    processor.process_files("./documents")
except Exception as e:
    print(f"处理文件时出错: {e}")

# 验证处理结果
searcher = processor.vector_searcher
print("\n=== 验证向量存储 ===")

# 列出所有集合
collections = searcher.list_collections()
print(f"\n找到的集合: {collections}")

# 检查每个集合的内容
for collection_name in collections:
    try:
        collection = searcher._ensure_collection(collection_name)
        collection_data = collection.get()
        collection_info = searcher.get_collection_info(collection_name)
        
        print(f"\n集合 '{collection_name}' 的详细信息:")
        print(f"- 文档数量: {collection_info.get('count', 0)}")
        if collection_data and collection_data.get('ids'):
            print(f"- 文档 IDs: {collection_data['ids'][:5]}... (显示前5个)")
        
        # 尝试搜索以验证内容
        test_query = "test"
        results = searcher.search(
            query=test_query,
            collection_names=[collection_name],
            top_k=1
        )
        if results and collection_name in results:
            print(f"- 搜索测试成功: 找到 {len(results[collection_name])} 个结果")
        else:
            print("- 搜索测试: 未找到结果")
    except Exception as e:
        print(f"检查集合 '{collection_name}' 时出错: {str(e)}")

# 检查 ChromaDB 客户端状态
print("\n=== ChromaDB 客户端状态 ===")
collection_names = searcher.client.list_collections()
print(f"ChromaDB 中的集合数量: {len(collection_names)}")
for name in collection_names:
    try:
        collection = searcher.client.get_collection(name)
        print(f"- 集合名称: {name}, 文档数量: {collection.count()}")
    except Exception as e:
        print(f"获取集合 '{name}' 信息时出错: {str(e)}")