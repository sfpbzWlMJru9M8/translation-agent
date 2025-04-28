

class Config(object):
    """应用程序全局配置类（继承自object确保新式类，Python 3中可省略）"""

    # Flask应用密钥，用于安全会话和加密操作
    # 生产环境必须修改此值，建议使用复杂随机字符串
    # 示例（不要使用）：'your-secret-key-here'，一般不加
    SECRET_KEY = 'sk-4ef934d0f93c40c7add1136dec67e690'
    # RAG模型API访问密钥
    # 需要从模型服务商处获取有效API KEY，可以去火山引擎官网申请，也可以去阿里百炼申请
    # 示例格式：'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    API_KEY = 'sk-4ef934d0f93c40c7add1136dec67e690'

    # 使用的RAG模型名称
    # 根据接入的模型服务商不同需要调整此参数
    # 示例：'deepseek-r1'，每个模型名称不同，具体请参考模型服务商文档
    MODEL = 'deepseek-r1'

    # 模型生成温度参数 (0.0-1.0)
    # 控制生成文本的随机性，值越高输出越随机有创意
    # 值越低输出越保守确定（推荐0.5-0.8之间）
    TEMPERATURE = 0.7

    # RAG API服务基础地址
    # 腾讯云API端点
    # 如果使用其他服务商需要替换对应地址
    BASE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
