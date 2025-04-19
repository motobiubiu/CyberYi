import streamlit as st
from web.chat_ui import ChatUI

class MeiHuaPage:
    def __init__(self, chat_ui: ChatUI):
        self.current_result = None
        self.chat_ui = chat_ui

    def meihua(self):
        """梅花易数功能"""
        self.current_result = "梅花易数功能开发中"
        return self.current_result

    def show_page(self):
        st.header("梅花易数")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.info("梅花易数功能开发中")
            if st.button("开始排盘"):
                result = self.meihua()
                self.chat_ui.show_divination_result(result)
                st.rerun()
        
        with col2:
            messages = self.chat_ui.setup_chat_ui()
            return messages
