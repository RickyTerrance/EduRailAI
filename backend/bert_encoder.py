# bert_encoder.py
"""
BERT模型編碼器
負責將文本轉換為向量表示
"""
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List
import logging

# 配置編碼器專用日誌
logger = logging.getLogger(__name__)
encoder_handler = logging.FileHandler(
    "logs/bert_encoder.log", encoding='utf-8')
encoder_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(encoder_handler)


class BERTEncoder:
    """BERT編碼器類別"""

    def __init__(self, model_name: str = "bert-base-chinese"):
        """
        初始化BERT編碼器
        載入預訓練模型和tokenizer
        """
        logger.info(f"正在初始化BERT編碼器，使用模型: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            logger.info(f"BERT編碼器初始化完成，使用設備: {self.device}")
        except Exception as e:
            logger.error(f"BERT編碼器初始化失敗: {str(e)}")
            raise

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        將文本列表轉換為向量表示

        參數:
            texts: 要編碼的文本列表
        返回:
            文本的向量表示數組
        """
        logger.info(f"開始編碼 {len(texts)} 個文本")
        encoded_texts = []
        for i, text in enumerate(texts):
            try:
                # 將文本轉換為模型輸入格式
                inputs = self.tokenizer(text, return_tensors="pt",
                                        max_length=512, truncation=True, padding=True)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

                # 生成文本向量表示
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    embeddings = outputs.last_hidden_state.mean(dim=1)
                    encoded_texts.append(embeddings.cpu().numpy().squeeze())

                if (i + 1) % 100 == 0:
                    logger.info(f"已完成 {i + 1}/{len(texts)} 個文本的編碼")

            except Exception as e:
                logger.error(f"編碼第 {i + 1} 個文本時發生錯誤: {str(e)}")
                raise

        logger.info("文本編碼完成")
        return np.array(encoded_texts)
