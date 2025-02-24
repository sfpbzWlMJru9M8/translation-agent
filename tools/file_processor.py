import os
from pathlib import Path
import hashlib
from concurrent.futures import ThreadPoolExecutor
import json
from typing import List, Set, Dict, Any
from langchain_community.document_loaders import (
    TextLoader,
    PDFMinerLoader,
    UnstructuredWordDocumentLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import ModelScopeEmbeddings
import logging
import torch
from docx2python import docx2python
import pandas as pd
from tools.vector_searcher import VectorSearcher

class FileProcessor:
    def __init__(self, 
                 persist_dir: str, 
                 collection_name: str = "translations",
                 max_workers: int = 4,
                 chunk_size: int = 500,
                 chunk_overlap: int = 50):
        """
        初始化文件处理器
        
        Args:
            persist_dir: 向量存储持久化目录
            collection_name: 向量存储集合名称
            max_workers: 最大并发工作线程数
            chunk_size: 文本分块大小
            chunk_overlap: 文本分块重叠大小
        """
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.max_workers = max_workers
        self.processed_files_path = os.path.join(persist_dir, f"{collection_name}_processed_files.json")
        
        # 使用 ModelScope 中文嵌入模型
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.embeddings = ModelScopeEmbeddings(
            model_id="damo/nlp_corom_sentence-embedding_chinese-base",
        )
        
        # 初始化向量存储
        self.vector_searcher = VectorSearcher(persist_dir=persist_dir)
        
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", ".", "!", "?", "！", "？", " ", ""]
        )
        
        # 设置日志
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"{__name__}.{collection_name}")
        
        # 加载已处理文件记录
        self.processed_files = self._load_processed_files()
        
        # 支持的文件类型及其加载器
        self.file_loaders = {
            '.txt': TextLoader,
            '.pdf': PDFMinerLoader,
            '.doc': UnstructuredWordDocumentLoader,
            '.docx': UnstructuredWordDocumentLoader
        }
        
        self.logger.info(f"初始化文件处理器: 集合名称={collection_name}, 存储目录={persist_dir}")
    
    def _load_processed_files(self) -> Set[str]:
        """加载已处理文件的记录"""
        if os.path.exists(self.processed_files_path):
            with open(self.processed_files_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()
    
    def _save_processed_files(self):
        """保存已处理文件的记录"""
        with open(self.processed_files_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.processed_files), f)
    
    def _get_file_hash(self, file_path: str) -> str:
        """计算文件的MD5哈希值"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _process_single_file(self, file_path: str) -> bool:
        """处理单个文件"""
        try:
            file_path = str(file_path)
            file_hash = self._get_file_hash(file_path)
            
            # 检查文件是否已处理
            if file_hash in self.processed_files:
                self.logger.info(f"文件已处理，跳过: {file_path}")
                return False
            
            # 获取文件扩展名
            ext = os.path.splitext(file_path)[1].lower()
            
            # 根据文件类型选择处理方法
            if ext == '.docx':
                self._process_docx(file_path)
            elif ext in ('.xlsx', '.xls'):
                self._process_excel(file_path)
            elif ext == '.json':
                self._process_json(file_path)
            elif ext in self.file_loaders:
                # 使用通用加载器处理其他支持的文件类型
                loader = self.file_loaders[ext](file_path)
                documents = loader.load()
                texts = self.text_splitter.split_documents(documents)
                self.vector_searcher.add_texts(
                    collection_name=self.collection_name,
                    texts=texts,
                    metadatas=[{"source": file_path} for _ in texts]
                )
            else:
                self.logger.warning(f"不支持的文件类型: {file_path}")
                return False
            
            # 记录已处理文件
            self.processed_files.add(file_hash)
            self._save_processed_files()
            
            self.logger.info(f"成功处理文件: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"处理文件失败 {file_path}: {str(e)}")
            return False
    
    def process_files(self, directory: str):
        """并发处理目录下的所有文件"""
        try:
            # 获取所有支持的文件
            files_to_process = []
            for ext in self.file_loaders.keys():
                files_to_process.extend(Path(directory).rglob(f"*{ext}"))
            
            if not files_to_process:
                self.logger.warning(f"目录中没有找到支持的文件: {directory}")
                return
            
            # 使用线程池并发处理文件
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                results = list(executor.map(self._process_single_file, files_to_process))
            
            # 统计处理结果
            processed = sum(1 for r in results if r)
            self.logger.info(f"处理完成: 成功 {processed} 个文件, 总计 {len(files_to_process)} 个文件")
            
        except Exception as e:
            self.logger.error(f"处理目录失败 {directory}: {str(e)}")
            raise
    
    def _process_docx(self, file_path: str) -> None:
        """处理Word文档"""
        try:
            # 使用 docx2python 提取文本
            with docx2python(file_path) as doc:
                text_content = []
                # 提取所有文本内容
                for paragraph in doc.text.split('\n'):
                    if paragraph.strip():
                        text_content.append(paragraph.strip())
            
            # 分割文本
            chunks = self.text_splitter.split_text("\n".join(text_content))
            
            # 添加到向量存储
            self.vector_searcher.add_texts(
                collection_name=self.collection_name,
                texts=chunks,
                metadatas=[{"source": file_path} for _ in chunks]
            )
            
            self.logger.info(f"成功处理Word文档: {file_path}")
            
        except Exception as e:
            self.logger.error(f"处理Word文档失败 {file_path}: {str(e)}")
            raise
    
    def _process_excel(self, file_path: str) -> None:
        """处理Excel文件"""
        try:
            # 读取所有sheet
            df = pd.read_excel(file_path, sheet_name=None)
            
            all_texts = []
            # 处理每个sheet
            for sheet_name, sheet_df in df.items():
                # 将每行转换为文本
                for _, row in sheet_df.iterrows():
                    row_text = " ".join(str(cell) for cell in row if pd.notna(cell))
                    if row_text.strip():
                        all_texts.append(row_text)
            
            # 分割文本
            chunks = self.text_splitter.split_text("\n".join(all_texts))
            
            # 添加到向量存储
            self.vector_searcher.add_texts(
                collection_name=self.collection_name,
                texts=chunks,
                metadatas=[{"source": file_path} for _ in chunks]
            )
            
            self.logger.info(f"成功处理Excel文件: {file_path}")
            
        except Exception as e:
            self.logger.error(f"处理Excel文件失败 {file_path}: {str(e)}")
            raise
    
    def _process_json(self, file_path: str) -> None:
        """处理JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 将JSON数据转换为文本
            texts = self._json_to_texts(data)
            
            # 分割文本
            chunks = self.text_splitter.split_text("\n".join(texts))
            
            # 添加到向量存储
            self.vector_searcher.add_texts(
                collection_name=self.collection_name,
                texts=chunks,
                metadatas=[{"source": file_path} for _ in chunks]
            )
            
            self.logger.info(f"成功处理JSON文件: {file_path}")
            
        except Exception as e:
            self.logger.error(f"处理JSON文件失败 {file_path}: {str(e)}")
            raise
    
    def _json_to_texts(self, data: Any) -> List[str]:
        """将JSON数据转换为文本列表"""
        texts = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    texts.extend(self._json_to_texts(value))
                else:
                    texts.append(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                texts.extend(self._json_to_texts(item))
        else:
            texts.append(str(data))
        
        return texts

    def _process_pdf(self, file_path: str) -> None:
        """处理PDF文件"""
        try:
            loader = PDFMinerLoader(file_path)
            pages = loader.load()
            
            # 提取文本
            text_content = []
            for page in pages:
                if isinstance(page, str):
                    text_content.append(page)
                elif hasattr(page, 'page_content'):
                    text_content.append(page.page_content)
            
            if not text_content:
                self.logger.warning(f"PDF文件没有提取到文本: {file_path}")
                return
            
            # 分割文本
            chunks = self.text_splitter.split_text("\n".join(text_content))
            
            if not chunks:
                self.logger.warning(f"文本分割后没有内容: {file_path}")
                return
            
            # 添加到向量存储
            try:
                self.vector_searcher.add_texts(
                    collection_name=self.collection_name,
                    texts=chunks,
                    metadatas=[{"source": file_path} for _ in chunks]
                )
                self.logger.info(f"成功处理PDF文件: {file_path}")
                
                # 记录已处理文件
                file_hash = self._get_file_hash(file_path)
                self.processed_files.add(file_hash)
                self._save_processed_files()
                
            except Exception as e:
                self.logger.error(f"添加文本到向量存储失败: {str(e)}")
                raise
            
        except Exception as e:
            self.logger.error(f"处理PDF文件失败 {file_path}: {str(e)}")
            raise 