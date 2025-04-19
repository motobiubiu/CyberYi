from typing import Any, Dict, List, Optional, Union
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import requests
from web.config import MODEL_CONFIG, CURRENT_MODEL

class CustomChatModel(BaseChatModel):
    """支持多供应商的聊天模型封装"""
    
    provider: str = "deepseek"
    model_name: str = "deepseek-chat"
    api_key:str = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    
    def __init__(self, provider: str = None,api_key: str=None,model:str=None, **kwargs):
        super().__init__(**kwargs)
        if provider:
            self.provider = provider
            self.model_name = model
            self.api_key = api_key
    
    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """处理单轮聊天请求"""
        result = self._generate(messages, stop=stop, **kwargs)
        return result.generations[0].text
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """生成聊天响应"""
        # 获取当前模型配置
        config = MODEL_CONFIG[self.provider]
        
        # 转换消息格式为API所需格式
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                formatted_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                formatted_messages.append({"role": "assistant", "content": msg.content})
        
        # 调用API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            **kwargs
        }
        
        response = requests.post(
            config["api_url"],
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        # 解析响应
        response_data = response.json()
        message = response_data["choices"][0]["message"]
        
        # 返回ChatResult
        generation = ChatGeneration(
            message=AIMessage(content=message["content"])
        )
        return ChatResult(generations=[generation])
    
    @property
    def _llm_type(self) -> str:
        """返回LLM类型标识"""
        return f"{self.provider}-chat"
