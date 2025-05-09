from typing import List, Optional, Dict, Any
import os
from openai import OpenAI
from tools.vector_searcher import VectorSearcher
import logging
import json

class RAGTranslator:
    def __init__(
        self,
        api_key: str,
        persist_dir: str,
        base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        model: str = "deepseek-r1",
        temperature: float = 0.7,
        source_lang: str = "英语",
        target_lang: str = "中文"
    ):
        """
        初始化RAG翻译器
        
        Args:
            api_key: API密钥
            persist_dir: 向量存储目录
            base_url: API基础URL
            model: 模型名称
            temperature: 温度参数
            source_lang: 源语言
            target_lang: 目标语言
        """
        # 初始化日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        self.model = model
        self.temperature = temperature
        
        # 初始化向量搜索器
        self.vector_searcher = VectorSearcher(persist_dir=persist_dir)
        
        # 设置语言
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        # 修改系统提示模板，确保格式更清晰
        self.system_prompt = """你是一个专业的翻译专家。请将{source_lang}翻译成{target_lang}。

请严格按照以下格式输出：

【翻译结果】
{text}的准确翻译内容。请直接给出翻译，不要添加任何额外的解释。

【翻译解析】
详细解释翻译过程，包括：
1. 词语选择的具体原因
2. 语境和语义的深入理解
3. 文化差异和语言特点的处理方法

参考资料：
{similar_translations}

重要提示：
- 必须按照上述格式输出
- 翻译结果要准确、地道
- 翻译解析要专业、详细
- 可参考资料，但不要完全依赖"""
    
    def _format_similar_translations(self, similar_results: List[dict]) -> str:
        """格式化相似翻译结果"""
        if not similar_results:
            return "没有找到相似的翻译参考。"
        
        formatted = []
        for i, result in enumerate(similar_results, 1):
            content = result['content']
            similarity = result['similarity']
            formatted.append(f"参考 {i} (相似度: {similarity:.2f}):\n{content}\n")
        
        return "\n".join(formatted)
    
    def translate_with_explanation(
        self,
        text: str,
        collection_names: Optional[List[str]] = None,
        top_k: int = 3,
        similarity_threshold: float = 0.5
    ) -> Dict[str, Any]:
        """翻译文本并提供详细解析"""
        try:
            # 获取相似文本
            search_results = self.vector_searcher.search(
                query=text,
                collection_names=collection_names,
                top_k=top_k,
                threshold=similarity_threshold
            )
            
            # 整合所有集合的结果
            all_similar_results = []
            for collection_results in search_results.values():
                all_similar_results.extend(collection_results)
            
            # 按相似度排序
            all_similar_results.sort(key=lambda x: x['similarity'], reverse=True)

            # 格式化相似翻译
            similar_translations = self._format_similar_translations(all_similar_results[:top_k])
            # print("=======================================参考内容=========================================")
            # print(similar_translations)
            # print("=========================================================================================")
            # 在使用时才进行格式化
            formatted_prompt = self.system_prompt.format(
                source_lang=self.source_lang,
                target_lang=self.target_lang,
                text=text,
                similar_translations=similar_translations
            )
            
            # 创建聊天完成
            completion = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": formatted_prompt},
                    {"role": "user", "content": text}
                ]
            )
            
            # 获取思考链内容
            thinking_process = completion.choices[0].message.reasoning_content
            translation_content = completion.choices[0].message.content
            
            # 解析翻译内容
            sections = translation_content.split('【')
            result = {
                'translation': '',
                'translation_reasoning': None,  # 初始化为 None
                'thinking_process': thinking_process  # 思考链内容
            }
            
            # 解析翻译结果和翻译解析
            for section in sections:
                if '翻译结果】' in section:
                    result['translation'] = section.split('】', 1)[1].strip()
                elif '翻译解析】' in section:
                    # 保存模型回复中的翻译解析
                    analysis = section.split('】', 1)[1].strip()
                    if analysis and analysis != thinking_process:  # 确保不是思考链内容
                        result['translation_reasoning'] = analysis
            
            return result
            
        except Exception as e:
            self.logger.error(f"翻译和解析失败: {str(e)}")
            raise

    def translate_stream(
        self,
        text: str,
        collection_names: Optional[List[str]] = None,
        top_k: int = 3,
        similarity_threshold: float = 0.5
    ):
        """流式翻译并提供实时输出"""
        try:
            # 获取相似文本
            search_results = self.vector_searcher.search(
                query=text,
                collection_names=collection_names,
                top_k=top_k,
                threshold=similarity_threshold
            )
            
            all_similar_results = []
            for collection_results in search_results.values():
                all_similar_results.extend(collection_results)
            
            all_similar_results.sort(key=lambda x: x['similarity'], reverse=True)
            similar_translations = self._format_similar_translations(all_similar_results[:top_k])
            
            # 在使用时才进行格式化
            formatted_prompt = self.system_prompt.format(
                source_lang=self.source_lang,
                target_lang=self.target_lang,
                text=text,
                similar_translations=similar_translations
            )
            
            # 记录日志
            self.logger.info(f"系统提示: {formatted_prompt}")
            
            # 创建流式聊天完成
            stream = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": formatted_prompt},
                    {"role": "user", "content": text}
                ],
                stream=True
            )
            
            return stream
            
        except Exception as e:
            self.logger.error(f"流式翻译失败: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            raise 