# translation-agent

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An intelligent translation system with context awareness and domain-specific adaptation capabilities, built with Python and HTML.

---

#### 🌟 Features

- **Multi-source Translation**: Integrates multiple translation APIs and local models to provide the best translation results
- **Context-aware Processing**: Considers full context to avoid isolated sentence translation issues
- **Domain Adaptation**: Special handling for technical documents, legal texts, and other specialized content
- **Interactive Correction**: Real-time feedback mechanism allowing users to participate in translation optimization
- **User-friendly Interface**: Simple, responsive web interface for a smooth translation experience

---

#### 📋 System Requirements

- Python 3.8+
- Flask
- Transformers
- Modern web browser
- Supports OpenAI and Alibaba BaiLian APIs (optional selection)

---

#### 🚀 Installation Guide

1. Clone the repository:

    ```bash
    git clone https://github.com/sfpbzWlMJru9M8/translation-agent.git
    cd translation-agent
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    # For Windows
    venv\Scripts\activate
    # For macOS/Linux
    source venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set API Keys (optional):

    Create a `.env` file in the project root directory and add your API keys:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ALIBABA_API_KEY=your_alibaba_api_key
    ALIBABA_API_SECRET=your_alibaba_api_secret
    ```

---

#### 🖥️ Usage Instructions

1. Start the server:

    ```bash
    python app.py
    ```

2. Open your browser and visit:

    ```
    http://localhost:5000
    ```

3. Select the source and target languages, input your text, and click "Translate".

---

#### 🧩 Project Structure

```
translation-agent/
├── app.py                        # Main Flask application
├── config.py                     # Configuration file
├── document_db                   # Document database
│   ├── bf02f15b-e7b8-409b-a5be-8b3dd93c8bc4
│   │   ├── data_level0.bin        # Binary data for document level 0
│   │   ├── header.bin             # Header information binary
│   │   ├── length.bin             # Length information binary
│   │   └── link_lists.bin         # Linked list binary
│   ├── chroma.sqlite3             # Chroma database (SQLite format)
│   └── translations_processed_files.json # Processed translations metadata
├── documents                     # Documents directory
│   └── aideng.pdf                 # Example document
├── example.py                    # Example script
├── process_example.py            # Example processing script
├── rag_translate_example.py      # RAG translation example script
├── read_structure.py             # Script to read project structure
├── requirements.txt              # Python dependencies list
├── search_example.py             # Example search script
├── templates                     # HTML templates directory
│   └── index.html                # Main page template
├── tools                         # Utility scripts
│   ├── file_processor.py          # File processor module
│   ├── rag_translator.py          # RAG translator module
│   └── vector_searcher.py         # Vector searcher module
├── translation-agent-en.md       # English documentation
├── translation-agent-zh.md       # Chinese documentation
└── uploads                       # Uploads directory
    └── r2.pdf                     # Uploaded PDF file

```





##### Translation Output Format

【Translation Result】
The corresponding translation result

【Thinking Chain】
Detailed process of the thinking chain

【Translation Analysis】
Detailed explanation of the translation process, including:

1. Specific reasons for word choices
2. Deep understanding of context and semantics
3. Handling methods for cultural differences and language features

#### 📧 Contact

[jony187423@gmail.com](mailto:jony187423@gmail.com)

* ​																			Last updated: 2025-04-27*