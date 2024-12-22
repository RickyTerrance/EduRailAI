# enhanced_agent.py
import httpx
import asyncio
from datetime import datetime
from typing import Dict, Optional
from fastapi import HTTPException
import logging
from pathlib import Path

from models import ChatRequest, ChatResponse
from bert_encoder import BERTEncoder
from rag_retriever import RAGRetriever
from prompt_template import PromptTemplate
from metrics_logger import MetricsLogger

logger = logging.getLogger(__name__)


class EnhancedOllamaAgent:
    def __init__(self, csv_path: str):

        self.encoder = BERTEncoder()
        self.retriever = RAGRetriever(csv_path, self.encoder)
        self.metrics_logger = MetricsLogger()
        self.ollama_url = "http://127.0.0.1:11434/api/chat"
        self.similarity_threshold = 0.5

        self.system_prompt = """
        您是一個回覆繁體中文的學習與職涯輔導平台"EduRail"的專業輔導師助理 EduRailAI。
        請遵守以下回覆原則：
        1. 回覆使用繁體中文。
        2. 使用條列式呈現資訊。
        3. 回覆簡潔明確，避免冗長。
        """

    async def _query_ollama(self, request: ChatRequest, context: Optional[str] = None) -> Dict:
        try:
            prompt = request.message
            if context:
                prompt = f"{context}\n\n使用者問題：{request.message}"

            payload = {
                "model": "llama3",
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }

            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.ollama_url,
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                )
                response.raise_for_status()
                return response.json()

        except httpx.RequestError as e:
            logger.error(f"Ollama服務連線錯誤: {str(e)}")
            raise HTTPException(status_code=503, detail="AI服務暫時無法連線")
        except Exception as e:
            logger.error(f"查詢Ollama時發生錯誤: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    async def process_query(self, request: ChatRequest) -> ChatResponse:
        start_time = datetime.now()
        try:
            # 1. 先嘗試RAG檢索
            rag_results = self.retriever.retrieve(request.message)

            # 2. 檢查RAG結果是否足夠相關
            if rag_results and rag_results[0]["similarity_score"] > self.similarity_threshold:
                # 使用RAG結果生成上下文
                context = PromptTemplate.generate_prompt(
                    request.message,
                    "\n\n".join([f"【{r['group_name']}】\n{r['introduction']}\n{r['learning_content']}"
                                for r in rag_results])
                )

                # 使用增強上下文查詢Ollama
                ollama_response = await self._query_ollama(request, context)

                response = ChatResponse(
                    response=ollama_response['message']['content'],
                    source="RAG+Ollama",
                    matched_groups=[r["group_name"] for r in rag_results]
                )
            else:
                # 3. 如果RAG結果不夠相關，直接使用Ollama
                ollama_response = await self._query_ollama(request)
                response = ChatResponse(
                    response=ollama_response['message']['content'],
                    source="Ollama",
                    matched_groups=None
                )

            # 4. 記錄指標
            end_time = datetime.now()
            metrics = self.metrics_logger.log_metrics(
                start_time, end_time,
                len(request.message),
                len(response.response)
            )
            response.metrics = metrics

            return response

        except Exception as e:
            logger.error(f"處理查詢時發生錯誤: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
