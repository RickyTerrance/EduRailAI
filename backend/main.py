# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import asyncio
from pathlib import Path

from models import ChatRequest, ChatResponse
from enhanced_agent import EnhancedOllamaAgent
from metrics_logger import MetricsLogger

# 配置日誌目錄
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 配置主日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "eduraid_ai.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 配置其他日誌
for log_name in ['model_monitor', 'gpu_monitor']:
    log_handler = logging.FileHandler(
        log_dir / f"{log_name}.log", encoding='utf-8')
    log_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger(log_name).addHandler(log_handler)

# 初始化FastAPI應用
app = FastAPI(
    title="EduRail AI Assistant API",
    description="Enhanced EduRail AI Assistant API with RAG-first approach",
    version="1.0.0"
)

# 添加CORS中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化代理和監控器
csv_path = 'college_details_ALL.csv'  # 根據實際路徑調整
agent = EnhancedOllamaAgent(csv_path)
metrics_logger = MetricsLogger()


@app.on_event("startup")
async def startup_event():
    """服務啟動初始化"""
    logger.info("服務啟動中...")
    # 可以在這裡添加其他初始化任務


@app.get("/")
async def root():
    """根路徑接口"""
    return {
        "service": "EduRail AI Assistant",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """增強版聊天接口"""
    try:
        return await agent.process_query(request)
    except Exception as e:
        logger.error(f"處理聊天請求時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
