from tools.rag_translator import RAGTranslator

# 初始化翻译器
translator = RAGTranslator(
    api_key="sk-zFmodcOHRQQ2P97XlMpsENO4LOv2gB8LH0SutfLidQ3fcXgz",
    persist_dir="./document_db",  # 使用之前创建的向量存储
    base_url="https://api.lkeap.cloud.tencent.com/v1",
    model="deepseek-r1",
    temperature=0.7,
    source_lang="英语",
    target_lang="中文"
)

# 测试翻译
text = """
Machine learning is an approach to artificial intelligence that enables computers 
to learn from data without being explicitly programmed. It has revolutionized 
many fields, from computer vision to natural language processing.
"""

# 从指定集合中搜索相似文本并翻译
translation = translator.translate(
    text=text,
    collection_names=["my_documents"],  # 指定要搜索的集合
    top_k=3,  # 使用前3个最相似的结果
    similarity_threshold=0.5  # 相似度阈值
)

print("\n最终翻译结果:")
print(translation) 