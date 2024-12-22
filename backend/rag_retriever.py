# rag_retriever.py
"""
RAG檢索器
負責從文檔集合中檢索相關內容
"""
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from typing import List, Dict
import logging
import bert_encoder

# 配置RAG檢索器專用日誌
logger = logging.getLogger(__name__)
retriever_handler = logging.FileHandler(
    "logs/rag_retriever.log", encoding='utf-8')
retriever_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(retriever_handler)


class RAGRetriever:
    """RAG檢索系統類別"""

    def __init__(self, csv_path: str, encoder: bert_encoder):
        """
        初始化RAG檢索器

        參數:
            csv_path: 學群資料CSV檔案路徑
            encoder: BERT編碼器實例
        """
        logger.info(f"初始化RAG檢索器，使用資料檔案: {csv_path}")
        try:
            self.df = pd.read_csv(csv_path)
            logger.info(f"成功載入 {len(self.df)} 筆學群資料")
            self.encoder = encoder
            self.encoded_texts = None
            self._prepare_embeddings()
        except Exception as e:
            logger.error(f"初始化RAG檢索器時發生錯誤: {str(e)}")
            raise

    def _prepare_embeddings(self):
        """準備文檔的向量表示"""
        logger.info("開始準備文檔向量")
        try:
            # 合併相關欄位作為文檔內容
            texts = [f"{row['group_name']} {row['introduction']} {row['learning_content']}"
                     for _, row in self.df.iterrows()]

            logger.info(f"開始編碼 {len(texts)} 個文檔")
            self.encoded_texts = self.encoder.encode(texts)
            logger.info("文檔向量準備完成")

        except Exception as e:
            logger.error(f"準備文檔向量時發生錯誤: {str(e)}")
            raise

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        檢索相關文檔

        參數:
            query: 查詢文本
            top_k: 返回最相關的文檔數量

        返回:
            包含相關文檔信息的字典列表
        """
        logger.info(f"開始處理查詢: {query}")
        try:
            # 對查詢文本進行編碼
            query_embedding = self.encoder.encode([query])

            # 計算相似度
            similarities = cosine_similarity(
                query_embedding, self.encoded_texts)[0]
            logger.debug(
                f"計算得到的相似度範圍: {similarities.min():.4f} - {similarities.max():.4f}")

            # 獲取最相關的文檔
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            results = []

            for idx in top_indices:
                row = self.df.iloc[idx]
                result = {
                    "group_name": row["group_name"],
                    "introduction": row["introduction"],
                    "learning_content": row["learning_content"],
                    "similarity_score": float(similarities[idx])
                }
                results.append(result)
                logger.debug(
                    f"找到相關學群: {row['group_name']}, 相似度: {similarities[idx]:.4f}")

            logger.info(f"成功檢索到 {len(results)} 個相關文檔")
            return results

        except Exception as e:
            logger.error(f"檢索過程中發生錯誤: {str(e)}")
            raise
