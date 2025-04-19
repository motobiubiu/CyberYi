import streamlit as st
import random
from datetime import datetime
from web.chat_ui import ChatUI
from yiching import ichingshifa

class LiuYaoPage:
    def __init__(self, chat_ui: ChatUI):
        self.current_result = None
        self.gua_map = {
            "老阴": "6",
            "少阳": "7", 
            "少阴": "8",
            "老阳": "9"
        }
        self.chat_ui = chat_ui

    def show_page(self):
        st.header("六爻占卜")
        col1, col2 = st.columns([1, 3])
        
        with col1:
            method = st.selectbox("起卦方式", ["手动起卦", "时间起卦", "随机起卦"])
            
            if method == "手动起卦":
                self.show_manual_divination()
            elif method == "时间起卦":
                self.show_time_divination()
            elif method == "随机起卦":
                self.show_random_divination()
        
        with col2:
            messages = self.chat_ui.setup_chat_ui()
            return messages

    def liuyao_manual(self, yao6, yao5, yao4, yao3, yao2, yao1):
        """手动六爻排盘"""
        gua_str = "".join([self.gua_map[yao] for yao in [yao1, yao2, yao3, yao4, yao5, yao6]])
        current_time = datetime.now()
        ichingshifa.Iching().mget_bookgua_details(gua_str)
        result=ichingshifa.Iching().display_pan(current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute)
        
        self.current_result = f"""
六爻排盘结果（手动起卦）：
上爻：{yao6}
五爻：{yao5}
四爻：{yao4}
三爻：{yao3}
二爻：{yao2}
初爻：{yao1}

{result}
"""
        return self.current_result
    
    def liuyao_time(self,current_time):
        """时间六爻排盘"""
        ichingshifa.Iching().datetime_bookgua(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
        result = ichingshifa.Iching().display_pan(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute)
        self.current_result = f"""
六爻排盘结果（时间起卦）：
起卦时间：{current_time.strftime("%Y-%m-%d %H:%M:%S")}

{result}
"""
        return self.current_result
    
    def liuyao_random(self, random_yao):
        """随机六爻排盘"""
        gua_str = "".join([self.gua_map[yao] for yao in random_yao])
        current_time = datetime.now()
        ichingshifa.Iching().mget_bookgua_details(gua_str)
        result=ichingshifa.Iching().display_pan(current_time.year,current_time.month,current_time.day,current_time.hour,current_time.minute)
        self.current_result = f"""
六爻排盘结果（随机起卦）：
上爻：{random_yao[5]}
五爻：{random_yao[4]}
四爻：{random_yao[3]}
三爻：{random_yao[2]}
二爻：{random_yao[1]}
初爻：{random_yao[0]}

{result}
"""
        return self.current_result

    def show_manual_divination(self):
        yao6 = st.selectbox("上爻", ["少阳", "少阴", "老阳", "老阴"])
        yao5 = st.selectbox("五爻", ["少阳", "少阴", "老阳", "老阴"])
        yao4 = st.selectbox("四爻", ["少阳", "少阴", "老阳", "老阴"])
        yao3 = st.selectbox("三爻", ["少阳", "少阴", "老阳", "老阴"])
        yao2 = st.selectbox("二爻", ["少阳", "少阴", "老阳", "老阴"])
        yao1 = st.selectbox("初爻", ["少阳", "少阴", "老阳", "老阴"])
        
        if st.button("开始排盘"):
            result = self.liuyao_manual(yao6, yao5, yao4, yao3, yao2, yao1)
            self.chat_ui.show_divination_result(result)
            st.rerun()

    def show_time_divination(self):
        current_time = st.text("当前时间: " + st.session_state.get("current_time", ""))
        if "now_time" not in st.session_state:
            st.session_state.now_time = datetime.now()
            st.session_state.current_time = st.session_state.now_time.strftime("%Y-%m-%d %H:%M:%S")
            
        if st.button("刷新时间"):
            st.session_state.now_time = datetime.now()
            st.session_state.current_time = st.session_state.now_time.strftime("%Y-%m-%d %H:%M:%S")
            st.rerun()
            
        if st.button("开始排盘"):
            result = self.liuyao_time(st.session_state.now_time)
            self.chat_ui.show_divination_result(result)
            st.rerun()

    def show_random_divination(self):
        if "random_yao" not in st.session_state:
            st.session_state.random_yao = ["", "", "", "", "", ""]
        
        st.text("上爻: " + st.session_state.random_yao[5])
        st.text("五爻: " + st.session_state.random_yao[4])
        st.text("四爻: " + st.session_state.random_yao[3])
        st.text("三爻: " + st.session_state.random_yao[2])
        st.text("二爻: " + st.session_state.random_yao[1])
        st.text("初爻: " + st.session_state.random_yao[0])
        
        if st.button("随机"):
            options = ["少阳", "少阴", "老阳", "老阴"]
            st.session_state.random_yao = [random.choice(options) for _ in range(6)]
            st.rerun()
            
        if st.button("开始排盘"):
            result = self.liuyao_random(st.session_state.random_yao)
            self.chat_ui.show_divination_result(result)
            st.rerun()

    def get_result(self):
        """获取当前排盘结果"""
        return self.current_result
