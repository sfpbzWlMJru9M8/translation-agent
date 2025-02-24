# 移除不需要的导入
# from exceptions import PendingDeprecationWarning

from tools.rag_translator import RAGTranslator

# 初始化翻译器
translator = RAGTranslator(
    api_key="sk-zFmodcOHRQQ2P97XlMpsENO4LOv2gB8LH0SutfLidQ3fcXgz",  # 替换为你的 API key
    persist_dir="./document_db",  # 指定存储位置
    base_url="https://api.lkeap.cloud.tencent.com/v1",  # 指定 API 基础 URL
    model="deepseek-r1"  # 指定模型
)

# 测试翻译
text = "Hello, how are you?"
result = translator.translate_with_explanation(text)

print("=== 翻译测试 ===")
print(f"原文: {text}")
print(f"\n翻译结果: {result['translation']}")
print(f"\n翻译解析: {result['translation_reasoning']}")
print(f"\n思考过程: {result['thinking_process']}")

# 再次翻译相同文本会利用向量库中的参考
print("\n=== 再次翻译 ===")
result2 = translator.translate_with_explanation(text)
print(f"翻译结果: {result2['translation']}") 