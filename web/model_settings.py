import streamlit as st
import json
import os
from web.config import MODEL_CONFIG, CURRENT_MODEL

class ModelSettings:
    def __init__(self):
        if "model_provider" not in st.session_state:
            st.session_state.model_provider = CURRENT_MODEL
    
    def show_settings_page(self):
        """显示独立的模型设置页面"""
        st.title("模型设置")
        
        # 模型供应商选择
        provider = st.selectbox(
            "选择模型供应商",
            options=list(MODEL_CONFIG.keys()),
            index=list(MODEL_CONFIG.keys()).index(st.session_state.model_provider)
        )
        
        # API Key输入
        api_key = st.text_input(
            "API Key",
            value=MODEL_CONFIG[provider]["api_key"],
            type="password"
        )
        
        # 模型名称
        model_name = st.text_input(
            "模型名称",
            value=MODEL_CONFIG[provider]["model_name"]
        )
        
        # API URL
        api_url = st.text_input(
            "API URL",
            value=MODEL_CONFIG[provider]["api_url"]
        )
        
        # 嵌入模型设置
        st.subheader("嵌入模型设置")
        embedding_provider = st.selectbox(
            "嵌入模型供应商",
            options=["SiliconFlow"],
            index=0
        )
        
        embedding_api_key = st.text_input(
            "嵌入模型API Key",
            value=MODEL_CONFIG[embedding_provider]["embedding_api_key"],
            type="password"
        )
        
        embedding_model_name = st.text_input(
            "嵌入模型名称",
            value=MODEL_CONFIG[embedding_provider]["embedding_model_name"]
        )
        
        embedding_api_url = st.text_input(
            "嵌入模型API URL",
            value=MODEL_CONFIG[embedding_provider]["embedding_api_url"]
        )
        
        # 保存按钮
        if st.button("保存配置"):
            MODEL_CONFIG[provider]["api_key"] = api_key
            MODEL_CONFIG[provider]["model_name"] = model_name
            MODEL_CONFIG[provider]["api_url"] = api_url
            MODEL_CONFIG[embedding_provider]["embedding_api_key"] = embedding_api_key
            MODEL_CONFIG[embedding_provider]["embedding_model_name"] = embedding_model_name
            MODEL_CONFIG[embedding_provider]["embedding_api_url"] = embedding_api_url


            st.session_state.model_provider = provider
            
            # 保存到配置文件
            try:
                config_path = os.path.join(os.path.dirname(__file__), "config.py")
                with open(config_path, "w") as f:
                    f.write("# 在此文件中存储API密钥等敏感配置\n")
                    f.write("# 请勿将此文件提交到版本控制\n\n")
                    f.write("MODEL_CONFIG = ")
                    f.write(json.dumps(MODEL_CONFIG, indent=4))
                    f.write("\n\n# 当前使用的模型\n")
                    f.write(f"CURRENT_MODEL = \"{provider}\"\n")
                st.success("配置已保存!")
            except Exception as e:
                st.error(f"保存配置失败: {str(e)}")
                print(f"保存配置错误: {str(e)}")
            
        # 返回主页面按钮
        if st.button("返回主页面"):
            st.session_state.page = "main"
            st.rerun()
