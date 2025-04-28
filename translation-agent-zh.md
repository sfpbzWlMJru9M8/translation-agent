# translation-agent

![版本](https://img.shields.io/badge/version-1.0.0-blue)
![许可证](https://img.shields.io/badge/license-MIT-green)

一个具有上下文感知和领域特定适配功能的智能翻译系统，基于Python和HTML构建。

#### 🌟 特点

- **多源翻译**：整合多个翻译API和本地模型，提供最佳翻译结果
- **上下文感知处理**：考虑完整上下文，避免孤立句子翻译问题
- **领域适配**：针对技术文档、法律文本和其他专业内容提供专门处理
- **交互式修正**：实时反馈机制，允许用户参与翻译优化过程
- **用户友好界面**：简洁、响应式Web界面，提供流畅的翻译体验

#### 📋 系统要求

- Python 3.8+
- Flask
- Transformers
- 现代网页浏览器
- OpenAI 和 阿里百炼均可，可自行选择

#### 🚀 安装指南

1. 克隆仓库：

```bash
git clone https://github.com/sfpbzWlMJru9M8/translation-agent.git
cd translation-agent
```

2. 创建并激活虚拟环境：

```bash
python -m venv venv
# Windows系统
venv\Scripts\activate
# macOS/Linux系统
source venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 设置API密钥（可选）：

在项目根目录创建`.env`文件，添加您的API密钥：

```
OPENAI_API_KEY=your_openai_api_key
ALIBABA_API_KEY=your_alibaba_api_key
ALIBABA_API_SECRET=your_alibaba_api_secret
```

#### 🖥️ 使用方法

1. 启动服务器：

```bash
python app.py
```

2. 打开浏览器并访问 `http://localhost:5000`

3. 选择源语言和目标语言，输入文本，然后点击"翻译"

#### 🧩 项目结构

```
translation-agent/
├── app.py                        # 主Flask应用
├── config.py                     # 配置文件
├── document_db                   # 文档数据库
│   ├── bf02f15b-e7b8-409b-a5be-8b3dd93c8bc4
│   │   ├── data_level0.bin
│   │   ├── header.bin
│   │   ├── length.bin
│   │   └── link_lists.bin
│   ├── chroma.sqlite3
│   └── translations_processed_files.json
├── documents                     # 文档目录
│   └── aideng.pdf
├── example.py                    # 示例脚本
├── process_example.py            # 处理示例脚本
├── rag_translate_example.py      # RAG翻译示例脚本
├── read_structure.py             # 读取项目结构脚本
├── requirements.txt              # Python依赖
├── search_example.py             # 搜索示例脚本
├── templates                     # HTML模板
│   └── index.html                # 主页模板
├── tools                         # 工具目录
│   ├── file_processor.py         # 文件处理器
│   ├── rag_translator.py         # RAG翻译器
│   └── vector_searcher.py        # 向量搜索器
├── translation-agent-en.md       # 英文文档
├── translation-agent-zh.md       # 中文文档
└── uploads                       # 上传文件目录
    └── r2.pdf
```

#### 翻译输出格式

```
【翻译结果】
对应的翻译结果

【思考链】
 思考链的详细过程

【翻译解析】
详细解释翻译过程，包括：
1. 词语选择的具体原因
2. 语境和语义的深入理解
3. 文化差异和语言特点的处理方法
```



#### 📧 联系方式

jony187423@gmail.com



* ​                                      															最后更新: 2025-04-27*