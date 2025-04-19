import streamlit as st
from web.chat_ui import ChatUI, get_qa_history_chain
from web.model_settings import ModelSettings
from web.liuyao_page import LiuYaoPage
from web.meihua_page import MeiHuaPage

def main():
    # 初始化页面状态
    if "page" not in st.session_state:
        st.session_state.page = "liuyao"
    
    # 初始化聊天UI
    chat_ui = ChatUI()
    
    # 导航栏
    with st.sidebar:
        my_logo = "img/img.png"
        st.image(my_logo, width=200)
        
        st.write("🔮 六爻")
        if st.button("六爻", use_container_width=True):
            st.session_state.page = "liuyao"
            st.rerun()
            
        st.write("🌸 梅花易数")    
        if st.button("梅花易数", use_container_width=True):
            st.session_state.page = "meihua"
            st.rerun()
            
        st.write("⚙️ 模型设置")
        if st.button("模型设置", use_container_width=True):
            st.session_state.page = "settings"
            st.rerun()
    
    # 页面内容
    if st.session_state.page == "settings":
        model_settings = ModelSettings()
        model_settings.show_settings_page()
        return
    
    # 获取消息容器
    messages = None
    
    # 六爻页面
    if st.session_state.page == "liuyao":
        liuyao_page = LiuYaoPage(chat_ui)
        messages = liuyao_page.show_page()
    
    # 梅花易数页面
    elif st.session_state.page == "meihua":
        meihua_page = MeiHuaPage(chat_ui)
        messages = meihua_page.show_page()
    
    # 初始化问答链
    if "qa_history_chain" not in st.session_state:
        st.session_state.qa_history_chain = get_qa_history_chain()
    
    # 处理用户输入
    if messages and (prompt := st.chat_input("Say something")):
        answer = chat_ui.handle_user_input(
            prompt=prompt,
            chain=st.session_state.qa_history_chain,
            messages=messages
        )
        with messages.chat_message("ai"):
            output = st.write_stream(answer)
        st.session_state.messages.append(("ai", output))

if __name__ == "__main__":
    main()
