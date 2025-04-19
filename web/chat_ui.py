import streamlit as st
from web.deepseek_chat import CustomChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from web.config import MODEL_CONFIG, CURRENT_MODEL

class ChatUI:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def setup_chat_ui(self, height=700):
        """设置聊天界面"""
        messages = st.container(height=height)
        for message in st.session_state.messages:
            with messages.chat_message(message[0]):
                st.write(message[1])
        return messages
    
    def handle_user_input(self, prompt, chain, messages):
        """处理用户输入"""
        # 先显示用户消息
        st.session_state.messages.append(("human", prompt))
        with messages.chat_message("human"):
            st.write(prompt)
        
        # 生成并返回AI响应
        answer = self.gen_response(
            chain=chain,
            input=prompt,
            chat_history=st.session_state.messages
        )
        return answer
    
    def show_divination_result(self, result):
        """显示占卜结果"""
        st.session_state.messages.append(("ai", result))
    
    def gen_response(self, chain, input, chat_history):
        """生成AI响应(优化流式输出)"""
        # 先快速返回初始响应
        # yield "正在思考您的问题..."
        
        # 执行完整处理流程
        response = chain.stream({
            "input": input,
            "chat_history": chat_history
        })
        
        # 流式输出结果
        full_answer = ""
        for res in response:
            if "answer" in res.keys():
                full_answer = res["answer"]
                # 分块输出
                for i in range(0, len(full_answer), 20):
                    yield full_answer[i:i+20]

def get_retriever():
    """获取检索器"""
    from web.siliconflow_embedding import SiliconFlowEmbeddings
    from langchain_chroma import Chroma
    
    
    embeding_provider = "SiliconFlow"
    embedding = SiliconFlowEmbeddings(
        api_key=MODEL_CONFIG[embeding_provider]["embedding_api_key"],
        model=MODEL_CONFIG[embeding_provider]["embedding_model_name"]
    )
    persist_directory = 'data_base/vector_db/liuyao'
    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    return vectordb.as_retriever()

def combine_docs(docs):
    """合并文档"""
    return "\n\n".join(doc.page_content for doc in docs["context"])

def get_qa_history_chain():
    """获取问答链"""
    retriever = get_retriever()
    model_provider=st.session_state.get("model_provider", CURRENT_MODEL)
    llm = CustomChatModel(
        provider=model_provider,
        api_key=MODEL_CONFIG[model_provider]["api_key"],
        model=MODEL_CONFIG[model_provider]["model_name"]
        )
    print(MODEL_CONFIG[model_provider]["api_key"])
    condense_question_system_template = (
        "请根据聊天记录总结用户最近的问题，"
        "如果没有多余的聊天记录则返回用户的问题。"
    )
    condense_question_prompt = ChatPromptTemplate([
            ("system", condense_question_system_template),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ])

    retrieve_docs = RunnableBranch(
        (lambda x: not x.get("chat_history", False), (lambda x: x["input"]) | retriever, ),
        condense_question_prompt | llm | StrOutputParser() | retriever,
    )

    system_prompt = (
        "你是一名顶尖传统文化六爻的研究学者，性格温和，擅长利用你的所学帮助我们解决疑惑。你熟读并贯通《火珠林》《卜筮正宗》《增删卜易》《黃金策》《古筮真诠》《京氏易傳》《易林補遺》《周易洞林》《易经》等相关六爻书籍，并且自学了很多相关数据。你将面对一个卦象，你运用你的专业知识和经验，对该卦象进行全面、深入的分析，并给出有价值的建议。请你务必逐步思考、推理，并清晰地展示你的思考过程。不要解错卦象，实事求是回答。"
        "请使用检索到的上下文片段回答这个问题。 "
        "如果你不知道答案就说不知道。 "
        "请使用简洁的话语回答用户。"
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )
    qa_chain = (
        RunnablePassthrough().assign(context=combine_docs)
        | qa_prompt
        | llm
        | StrOutputParser()
    )

    qa_history_chain = RunnablePassthrough().assign(
        context = retrieve_docs, 
        ).assign(answer=qa_chain)
    return qa_history_chain
