import httpx
import logging
import json
from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import List, Dict, Optional
from datetime import datetime

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ollama_agent.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str

    @validator('message')
    def validate_message(cls, v):
        if len(v) > 1000:
            raise ValueError('訊息長度不可超過1000字')
        return v


class OllamaAgent:
    def __init__(self):
        self.conversation_history: List[Dict[str, str]] = []
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.max_history_length = 10

        self.system_prompt = """
        您是一個回覆繁體中文的學習與職崖輔導平台"EduRail"的專業輔導師助理 EduRailAI。
        請遵守以下回覆原則：

        1.回覆使用繁體中文。
        2.盡可能使用條列式（bullet points）呈現複雜的資訊
        3.保持回覆簡潔明確
        4.如果內容涉及多個層面，請使用清晰的標題和子標題
        5.如需學術或艱深的詞彙，請加以解釋
        6.若問題需要詳細解釋，請先提供摘要，再逐步展開
        7.單純打招呼可以多一些emoji活潑一點，也可以簡單自我介紹
        8.你的主要客群都是台灣的國小、國中、高中、大學生為主喔~
        9.請避免使用簡體中文、全英文
        10.使用者對你表達感激時，要說不客氣，感謝您的支持這類的話語。
        """

    async def chat(self, request: ChatRequest):
        """
        處理對話請求的非同步方法，增加詳細的錯誤處理和日誌記錄
        """
        start_time = datetime.now()
        logger.info(f"收到對話請求: {request.message}")

        try:
            # 輸入驗證
            if not request.message or len(request.message.strip()) == 0:
                logger.warning("收到空白訊息")
                raise HTTPException(status_code=400, detail="訊息不可為空")

            # 將使用者訊息加入對話歷史
            user_message = {
                "role": "user",
                "content": request.message,
                "timestamp": start_time.isoformat()
            }
            self.conversation_history.append(user_message)

            # 構建 Ollama 的 payload
            payload = {
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": request.message}
                ],
                "stream": False
            }

            # 發送請求到 Ollama
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.ollama_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )

                # 檢查請求是否成功
                response.raise_for_status()

                # 解析 Ollama 的回應
                ollama_response = response.json()
                response_text = ollama_response['message']['content']

                # 將 AI 回應加入對話歷史
                ai_message = {
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now().isoformat()
                }
                self.conversation_history.append(ai_message)

                # 限制對話歷史長度
                if len(self.conversation_history) > self.max_history_length:
                    self.conversation_history = self.conversation_history[-self.max_history_length:]

                # 記錄回應日誌
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"對話處理完成，耗時 {duration} 秒")

                # 記錄交談細節到日誌文件
                self._log_conversation(request.message, response_text)

                return {"response": response_text}

        except httpx.RequestError as e:
            logger.error(f"AI服務連線錯誤: {str(e)}")
            raise HTTPException(status_code=503, detail="AI服務暫時無法連線。")
        except Exception as e:
            logger.error(f"處理對話時發生未預期錯誤: {str(e)}")
            raise HTTPException(status_code=500, detail=f"發生意外錯誤：{str(e)}")

    async def reset_chat(self):
        """重置對話歷史，並記錄日誌"""
        logger.info("重置對話歷史")
        self.conversation_history = []
        return {"status": "對話歷史已重置"}

    def _log_conversation(self, user_message: str, ai_response: str):
        """將對話詳細資訊記錄到專門的對話日誌檔案"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "ai_response": ai_response
            }

            with open("conversation_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"記錄對話日誌時發生錯誤: {str(e)}")
