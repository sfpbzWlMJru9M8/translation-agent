from tools.translator_agent import TranslatorAgent

# 初始化翻译智能体
translator = TranslatorAgent(
    api_key="your-openai-api-key",
    persist_dir="./translation_db"  # 指定存储位置
)

# 测试翻译
text = "Hello, how are you?"
translation = translator.translate(text)
print(f"原文: {text}")
print(f"翻译: {translation}")

# 再次翻译相同文本会直接从向量库获取
translation2 = translator.translate(text)
print(f"\n从向量库获取的翻译: {translation2}") 