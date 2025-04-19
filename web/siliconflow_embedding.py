from langchain.embeddings.base import Embeddings
from typing import List
import requests

class SiliconFlowEmbeddings(Embeddings):
    def __init__(self, api_key: str, model: str = "BAAI/bge-m3"):
        self.api_key =api_key
        self.model = model
        self.url = "https://api.siliconflow.cn/v1/embeddings"

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        embeddings = []
        for text in texts:
            payload = {
                "model": self.model,
                "input": text,
                "encoding_format": "float"
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(self.url, json=payload, headers=headers)
            if response.status_code == 200:
                embeddings.append(response.json()["data"][0]["embedding"])
            else:
                raise ValueError(f"Embedding request failed: {response.text} code: {response.status_code}")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        return self.embed_documents([text])[0]
