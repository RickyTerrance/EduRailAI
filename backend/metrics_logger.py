# metrics_logger.py
from typing import Dict, List, Optional
import json
import logging
from datetime import datetime
import psutil
import GPUtil
from pathlib import Path

# 確保日誌目錄存在
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 配置指標記錄器專用日誌
logger = logging.getLogger(__name__)
metrics_handler = logging.FileHandler(
    log_dir / "metrics.log", encoding='utf-8')
metrics_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(metrics_handler)


class MetricsLogger:
    """效能指標記錄器類別"""

    def __init__(self):
        """初始化效能指標記錄器"""
        self.model_logger = logging.getLogger('model_monitor')
        self.gpu_logger = logging.getLogger('gpu_monitor')
        self.metrics_history = []
        logger.info("效能指標記錄器初始化完成")

    def log_metrics(self,
                    start_time: Optional[datetime] = None,
                    end_time: Optional[datetime] = None,
                    message_length: Optional[int] = None,
                    response_length: Optional[int] = None,
                    additional_metrics: Optional[Dict] = None) -> Dict:
        """
        記錄系統效能指標

        參數:
            start_time: 處理開始時間
            end_time: 處理結束時間
            message_length: 輸入訊息長度
            response_length: 回應訊息長度
            additional_metrics: 額外需要記錄的指標

        返回:
            包含所有記錄指標的字典
        """
        try:
            current_time = datetime.now()
            metrics = {
                "timestamp": current_time.isoformat(),
                "system_metrics": self.get_system_metrics(),
                "gpu_metrics": self.get_gpu_metrics()
            }

            # 如果提供了時間資訊，計算處理時間相關指標
            if start_time and end_time:
                duration = (end_time - start_time).total_seconds()
                metrics.update({
                    "processing_time": duration
                })

                # 如果提供了訊息長度資訊，計算處理速率
                if message_length is not None and response_length is not None:
                    metrics.update({
                        "message_length": message_length,
                        "response_length": response_length,
                        "tokens_per_second": (message_length + response_length) / duration
                    })

            # 添加額外指標
            if additional_metrics:
                metrics.update(additional_metrics)

            # 記錄到歷史
            self.metrics_history.append(metrics)

            # 如果歷史記錄太長，清理舊數據
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]

            # 記錄到日誌
            self.model_logger.info(
                f"模型指標: {json.dumps(metrics, ensure_ascii=False)}")

            return metrics

        except Exception as e:
            logger.error(f"記錄效能指標時發生錯誤: {str(e)}")
            return {}

    @staticmethod
    def get_gpu_metrics() -> List[Dict]:
        """
        獲取GPU使用指標

        返回:
            GPU使用情況指標列表
        """
        try:
            gpus = GPUtil.getGPUs()
            metrics = [{
                "id": gpu.id,
                "name": gpu.name,
                "load": f"{gpu.load*100:.1f}%",
                "memory_used": f"{gpu.memoryUsed}MB",
                "memory_total": f"{gpu.memoryTotal}MB",
                "temperature": f"{gpu.temperature}°C"
            } for gpu in gpus]
            logger.debug(f"GPU指標: {json.dumps(metrics, ensure_ascii=False)}")
            return metrics
        except Exception as e:
            logger.error(f"獲取GPU指標時發生錯誤: {str(e)}")
            return []

    @staticmethod
    def get_system_metrics() -> Dict:
        """
        獲取系統資源使用指標

        返回:
            系統資源使用情況指標
        """
        try:
            metrics = {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            }
            logger.debug(f"系統指標: {json.dumps(metrics, ensure_ascii=False)}")
            return metrics
        except Exception as e:
            logger.error(f"獲取系統指標時發生錯誤: {str(e)}")
            return {}

    def get_metrics_history(self) -> List[Dict]:
        """
        獲取歷史效能指標記錄

        返回:
            歷史效能指標記錄列表
        """
        return self.metrics_history

    def clear_metrics_history(self) -> None:
        """清空歷史效能指標記錄"""
        self.metrics_history = []
        logger.info("已清空歷史效能指標記錄")
