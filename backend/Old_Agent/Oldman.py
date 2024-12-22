import os
import sys
import logging
import signal
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 導入其他代理
from backend.Old_Agent.OllamaAgent import OllamaAgent
from backend.Old_Agent.BERTAgent import BertRAGAgent, RAGRequest

# 設置基本日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MainAgent:
    def __init__(self):
        # 初始化 FastAPI 應用
        self.app = FastAPI()

        # 配置 CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # 初始化各代理
        self.bert_agent = BertRAGAgent()
        self.ollama_agent = OllamaAgent()

        # 初始化工作流控制參數
        self.max_iterations = 5  # 最大迭代次數
        self.timeout_seconds = 60  # 超時時間

        # 註冊路由
        self._register_routes()
        self._register_workflow_routes()

    def _register_routes(self):
        """註冊所有 API 端點"""
        # Ollama 相關路由
        self.app.post("/api/chat")(self.ollama_agent.chat)
        self.app.post("/api/reset_chat")(self.ollama_agent.reset_chat)

        # BERT RAG 相關路由
        self.app.post("/api/college_rag")(self.bert_agent.college_rag_search)

    def _register_workflow_routes(self):
        """註冊工作流控制路由"""
        self.app.add_api_route(
            "/api/smart_route", self.smart_route, methods=["POST"])

    async def smart_route(self, request: Request):
        """智能路由，根據查詢選擇最佳Agent"""
        logger.info("進入了 smart_route 路由")

        try:
            # 獲取請求數據
            data = await request.json()
            query = data.get('query', '').strip()

            # 日誌記錄
            logger.info(f"收到智能路由查詢: {query}")

            # 若查詢為空，返回錯誤信息
            if not query:
                return JSONResponse(content={"response": "查詢內容不能為空，請提供有效問題"}, status_code=400)

            # 自省與路由邏輯
            iterations = 0
            while iterations < self.max_iterations:
                # 檢查查詢類型
                if self._is_college_related(query):
                    logger.info(f"查詢為學群相關，使用BERT RAG進行處理")
                    result = await self.bert_agent.college_rag_search(query)
                elif self._is_general_query(query):
                    logger.info(f"查詢為一般問題，使用Ollama進行處理")
                    result = await self.ollama_agent.chat(query)
                else:
                    logger.warning(f"無法識別的查詢類型: {query}")
                    result = {"response": "無法處理此類型查詢"}

                # 自我反思機制：檢查結果是否滿意
                if self._is_result_satisfactory(result):
                    logger.info(f"查詢結果滿意，返回結果")
                    return JSONResponse(content=result)

                iterations += 1
                logger.info(f"第{iterations}次迭代，未達到滿意結果，繼續處理")

            # 若達到最大迭代次數，返回部分結果
            logger.warning(f"達到最大迭代次數，未能完全解決查詢")
            return JSONResponse(content={"response": "未能完全解決您的查詢，建議重新詳細描述"}, status_code=500)

        except Exception as e:
            # 異常處理
            logger.error(f"處理查詢時出現錯誤: {str(e)}")
            return JSONResponse(content={"response": "系統處理錯誤，請稍後再試"}, status_code=500)

    def _is_college_related(self, query: str) -> bool:
        """判斷是否為學群相關查詢"""
        college_keywords = ['學群', '大學', '科系',
                            '選課', '升學', '領域', '科目', '系所', '學程']
        return any(keyword in query for keyword in college_keywords)

    def _is_general_query(self, query: str) -> bool:
        """判斷是否為一般查詢"""
        return len(query) > 0

    def _is_result_satisfactory(self, result: dict) -> bool:
        """簡單的結果滿意度評估"""
        # 可以根據結果長度、特定關鍵詞等進行評估
        return len(str(result)) > 50

    def graceful_shutdown(self, signum, frame):
        """優雅地關閉伺服器"""
        logger.info("收到關閉信號，正在優雅地關閉伺服器...")
        sys.exit(0)

    def run(self, host="0.0.0.0", port=8000):
        """啟動伺服器"""
        # 設置信號處理
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)

        logger.info(f"伺服器正在 {host}:{port} 啟動...")
        uvicorn.run(self.app, host=host, port=port)


# 創建 MainAgent 實例並導出 app
main_agent = MainAgent()
app = main_agent.app


def main():
    main_agent.run()


if __name__ == "__main__":
    main()
