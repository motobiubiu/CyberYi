# 在此文件中存储API密钥等敏感配置
# 请勿将此文件提交到版本控制

MODEL_CONFIG = {
    "deepseek": {
        "api_key": "",
        "model_name": "deepseek-chat",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "embedding_api_key": "",
        "embedding_model_name": "",
        "embedding_api_url": ""
    },
    "openai": {
        "api_key": "",
        "model_name": "gpt-3.5-turbo",
        "api_url": "https://api.openai.com/v1/chat/completions",
        "embedding_api_key": "",
        "embedding_model_name": "",
        "embedding_api_url": ""
    },
    "qwen": {
        "api_key": "",
        "model_name": "qwen-turbo",
        "api_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "embedding_api_key": "",
        "embedding_model_name": "",
        "embedding_api_url": ""
    },
    "SiliconFlow": {
        "api_key": "",
        "model_name": "",
        "api_url": "https://api.siliconflow.cn/v1/chat/completions",
        "embedding_api_key": "",
        "embedding_model_name": "BAAI/bge-m3",
        "embedding_api_url": "https://api.siliconflow.cn/v1/embeddings"
    }
}

# 当前使用的模型
CURRENT_MODEL = "deepseek"
