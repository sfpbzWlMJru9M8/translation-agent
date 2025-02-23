from langchain_community.embeddings import ModelScopeEmbeddings

import chromadb
import logging
from typing import List, Union, Dict, Optional
import os
import torch
from langchain_community.vectorstores import Chroma


class VectorSearcher:
    def __init__(self, persist_dir: str):
        """
        初始化向量查询器
        
        Args:
            persist_dir: 向量存储目录，需要与FileProcessor使用相同的目录
        """
        self.persist_dir = persist_dir
        
        # 使用 ModelScope 中文嵌入模型
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embeddings = ModelScopeEmbeddings(
            model_id="damo/nlp_corom_sentence-embedding_chinese-base",
        )
        
        # 确保存储目录存在
        os.makedirs(persist_dir, exist_ok=True)
        
        # 初始化 ChromaDB 客户端
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 存储已加载的集合
        self.collections: Dict[str, Chroma] = {}
        
    def _ensure_collection(self, collection_name: str) -> Chroma:
        """确保集合存在并返回集合对象"""
        if collection_name not in self.collections:
            try:
                # 尝试获取现有集合
                chroma_collection = self.client.get_or_create_collection(name=collection_name)
                
                # 创建或加载 Langchain Chroma 集合
                self.collections[collection_name] = Chroma(
                    client=self.client,
                    collection_name=collection_name,
                    embedding_function=self.embeddings,
                )
                self.logger.info(f"已加载/创建集合: {collection_name}")
            except Exception as e:
                self.logger.error(f"创建/加载集合失败 {collection_name}: {str(e)}")
                raise
        
        return self.collections[collection_name]
    
    def search(self, 
              query: str, 
              collection_names: Union[str, List[str]] = None,
              top_k: int = 5,
              threshold: float = 0.0) -> Dict[str, List[Dict]]:
        """
        在指定集合中搜索相似内容
        
        Args:
            query: 查询文本
            collection_names: 要搜索的集合名称，可以是单个名称或列表。None表示搜索所有已加载的集合
            top_k: 每个集合返回的最相似结果数量
            threshold: 相似度阈值，只返回相似度高于此值的结果
            
        Returns:
            Dict[str, List[Dict]]: 按集合名称组织的搜索结果
        """
        try:
            results = {}
            
            # 处理集合名称参数
            if isinstance(collection_names, str):
                collection_names = [collection_names]
            elif collection_names is None:
                collection_names = self.list_collections()
            
            for name in collection_names:
                # 确保集合已加载
                collection = self._ensure_collection(name)
                
                # 检查集合是否为空
                if not collection.get()['ids']:
                    self.logger.warning(f"集合 {name} 为空")
                    continue
                
                # 执行搜索
                docs_and_scores = collection.similarity_search_with_score(
                    query, k=top_k
                )
                
                # 处理结果
                collection_results = []
                for doc, score in docs_and_scores:
                    if score >= threshold:
                        collection_results.append({
                            'content': doc.page_content,
                            'metadata': doc.metadata,
                            'similarity': float(score)
                        })
                
                if collection_results:
                    results[name] = collection_results
                    
            return results
            
        except Exception as e:
            self.logger.error(f"搜索失败: {str(e)}")
            raise
    
    def list_collections(self) -> List[str]:
        """列出所有可用集合"""
        try:
            # 在 v0.6.0 中，list_collections 直接返回集合名称列表
            collection_names = self.client.list_collections()
            self.logger.info(f"找到 {len(collection_names)} 个集合: {collection_names}")
            return collection_names
        except Exception as e:
            self.logger.error(f"获取集合列表失败: {str(e)}")
            return []
    
    def get_collection_info(self, collection_name: str) -> Dict:
        """获取集合详细信息"""
        try:
            collection = self.client.get_collection(name=collection_name)
            return {
                'name': collection_name,
                'count': collection.count()
            }
        except Exception as e:
            self.logger.error(f"获取集合信息失败 {collection_name}: {str(e)}")
            return {}
    
    def add_texts(
        self,
        collection_name: str,
        texts: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """向指定集合添加文本"""
        try:
            if not texts:
                self.logger.warning("没有要添加的文本")
                return []
            
            # 处理文本
            processed_texts = []
            for text in texts:
                if hasattr(text, 'page_content'):
                    processed_texts.append(text.page_content)
                else:
                    processed_texts.append(str(text))
            
            # 生成唯一ID（如果未提供）
            if ids is None:
                import uuid
                ids = [str(uuid.uuid4()) for _ in processed_texts]
            
            # 确保集合存在并获取
            collection = self._ensure_collection(collection_name)
            
            # 添加文本到集合
            collection.add_texts(
                texts=processed_texts,
                metadatas=metadatas,
                ids=ids
            )
            
            # 验证添加是否成功
            count = len(collection.get()['ids']) if collection.get() else 0
            self.logger.info(f"成功添加 {len(texts)} 条文本到集合 {collection_name}")
            self.logger.info(f"集合 {collection_name} 现有 {count} 条记录")
            
            return ids
            
        except Exception as e:
            self.logger.error(f"添加文本到集合 {collection_name} 失败: {str(e)}")
            raise 