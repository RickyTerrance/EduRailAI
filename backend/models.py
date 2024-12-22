from typing import List, Dict, Optional
from pydantic import BaseModel, validator

# models.py
"""
定義系統使用的資料模型
包含請求和回應的資料結構定義
"""


class ChatRequest(BaseModel):
    """聊天請求的資料模型"""
    message: str

    @validator('message')
    def validate_message(cls, v):
        """
        驗證訊息內容
        確保訊息長度不超過限制且不為空
        """
        if len(v) > 1000:
            raise ValueError('訊息長度不可超過1000字')
        return v


class ChatResponse(BaseModel):
    """聊天回應的資料模型"""
    response: str           # 回應內容
    source: str            # 回應來源（RAG或Ollama）
    matched_groups: Optional[List[str]] = None  # 匹配到的學群名稱列表
    metrics: Optional[Dict] = None              # 效能指標資料
