from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from tools.rag_translator import RAGTranslator
from tools.file_processor import FileProcessor
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 初始化翻译器
translator = RAGTranslator(
    api_key="sk-zFmodcOHRQQ2P97XlMpsENO4LOv2gB8LH0SutfLidQ3fcXgz",
    persist_dir="./document_db",
    base_url="https://api.lkeap.cloud.tencent.com/v1",
    model="deepseek-r1",
    temperature=0.7
)

# 初始化文件处理器
file_processor = FileProcessor(
    persist_dir="./document_db",
    collection_name="translations"
)

@app.route('/')
def home():
    """渲染主页"""
    return render_template('index.html')

@app.route('/translate')
def translate():
    """处理翻译请求"""
    try:
        # 从查询参数获取数据
        text = request.args.get('text', '')
        source_lang = request.args.get('source_lang', '英语')
        target_lang = request.args.get('target_lang', '中文')
        
        if not text:
            return jsonify({'error': '请输入要翻译的文本'}), 400
        
        # 更新翻译器的语言设置
        translator.source_lang = source_lang
        translator.target_lang = target_lang
        
        def generate():
            try:
                stream = translator.translate_stream(
                    text=text,
                    collection_names=["translations"],
                    top_k=3,
                    similarity_threshold=0.5
                )
                
                translation_result = ''
                translation_reasoning = ''
                thinking_process = ''
                current_content = ''
                
                for chunk in stream:
                    print(f"DEBUG: Chunk received - {chunk}")
                    
                    # 处理思考链内容
                    if hasattr(chunk.choices[0].delta, 'reasoning_content'):
                        content = chunk.choices[0].delta.reasoning_content
                        if content:
                            thinking_process += content
                            print(f"DEBUG: Reasoning content - {content}")
                            yield f"data: {json.dumps({'type': 'thinking', 'content': content})}\n\n"
                    
                    # 处理翻译内容
                    if hasattr(chunk.choices[0].delta, 'content'):
                        content = chunk.choices[0].delta.content
                        if content:
                            print(f"DEBUG: Translation content - {content}")
                            current_content += content
                            
                            # 检查是否包含翻译结果标记
                            if '【翻译结果】' in current_content:
                                parts = current_content.split('【翻译结果】')
                                if len(parts) > 1:
                                    result_text = parts[1]
                                    if '【' in result_text:
                                        result_text = result_text.split('【')[0]
                                    translation_result = result_text.strip()
                                    yield f"data: {json.dumps({'type': 'translation', 'content': translation_result})}\n\n"
                            
                            # 检查是否包含翻译解析标记
                            if '【翻译解析】' in current_content:
                                parts = current_content.split('【翻译解析】')
                                if len(parts) > 1:
                                    analysis_text = parts[1]
                                    if '【' in analysis_text:
                                        analysis_text = analysis_text.split('【')[0]
                                    translation_reasoning = analysis_text.strip()
                                    yield f"data: {json.dumps({'type': 'analysis', 'content': translation_reasoning})}\n\n"
                
                # 发送完整响应
                result = {
                    'translation': translation_result,
                    'translation_reasoning': translation_reasoning,
                    'thinking_process': thinking_process
                }
                yield f"data: {json.dumps({'type': 'complete', 'data': result})}\n\n"
                
            except Exception as e:
                print(f"DEBUG: Error occurred - {str(e)}")
                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        
        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )
        
    except Exception as e:
        app.logger.error(f"翻译错误: {str(e)}")
        return jsonify({'error': f'翻译失败: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有上传文件'}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
            
        # 创建上传目录
        upload_dir = './uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_path = os.path.join(upload_dir, secure_filename(file.filename))
        file.save(file_path)
        
        # 处理文件
        try:
            file_processor.process_files(upload_dir)
            return jsonify({'message': '文件处理成功'})
        except Exception as e:
            return jsonify({'error': f'文件处理失败: {str(e)}'}), 500
        finally:
            # 清理上传文件
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        return jsonify({'error': f'文件上传失败: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)