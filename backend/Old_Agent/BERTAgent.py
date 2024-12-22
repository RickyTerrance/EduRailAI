import os
import torch
import logging
import numpy as np
import pandas as pd
from typing import List, Dict
from fastapi import HTTPException
from pydantic import BaseModel, validator
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import json

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bert_agent.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RAGRequest(BaseModel):
    query: str

    @validator('query')
    def validate_query(cls, v):
        if len(v) > 100:
            raise ValueError('查詢長度不可超過100字')
        return v


class PromptTemplate(BaseModel):
    """
    專門為大學學群 RAG 系統設計的提示模板管理類別
    """
    @staticmethod
    def load_predefined_prompts(file_path: str = 'predefined_prompts.json') -> Dict[str, str]:
        """
        載入預定義的提示模板
        """
        try:
            if not os.path.exists(file_path):
                # 如果檔案不存在，建立一個預設的提示模板
                default_prompts = {
                    "general_inquiry": "根據您的查詢「{query}」，我為您找到了以下最相關的學群資訊。請參考推薦，這些學群可能非常適合您的興趣和未來發展。",
                    "career_guidance": "您的查詢「{query}」顯示出對特定專業領域的興趣。以下學群推薦不僅提供學術知識，更能幫助您規劃未來職涯發展。",
                    "academic_exploration": "對於「{query}」的探索，我們為您精選了最匹配的學群。這些推薦將協助您更深入了解不同學術領域的特色和可能性。"
                }

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_prompts, f, ensure_ascii=False, indent=4)

            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"載入提示模板時發生錯誤: {e}")
            return {}

    @staticmethod
    def generate_enhanced_context(query: str, top_groups: List[Dict], prompt_type: str = "general_inquiry") -> str:
        """
        根據不同的提示類型，生成更豐富、更有針對性的上下文
        """
        # 載入提示模板
        prompts = PromptTemplate.load_predefined_prompts()
        base_prompt = prompts.get(prompt_type, prompts.get("general_inquiry"))

        # 根據提示類型客製化輸出
        context_intro = base_prompt.format(query=query) + "\n\n"
        context_intro += "🔍 智能推薦報告：精準匹配您的學術興趣\n\n"

        context_groups = ""
        for idx, group in enumerate(top_groups, 1):
            context_groups += f"🎓 推薦學群 {idx}：{group['group_name']}\n"
            context_groups += f"   • 學群特色：{group['introduction']}\n"
            context_groups += f"   • 課程亮點：{group['learning_content']}\n"
            context_groups += f"   • 相關領域：{group.get('related_groups', '尚未提供相關領域資訊')}\n"
            context_groups += f"   • 更多資訊：{group['link']}\n\n"

        context_outro = "💡 專業建議：\n"
        context_outro += "   • 深入研究每個推薦學群的完整介紹\n"
        context_outro += "   • 參考學群特色，評估是否符合個人興趣\n"
        context_outro += "   • 主動諮詢學校輔導老師，獲得更精準的選課建議\n"

        return context_intro + context_groups + context_outro

    @staticmethod
    def suggest_prompt_type(query: str) -> str:
        """
        根據查詢內容智能推薦提示模板類型
        """
        # 定義關鍵字映射
        keyword_mapping = {
            "career": ["職業", "工作", "未來", "就業", "職涯"],
            "academic": ["學術", "研究", "領域", "專業", "學問"]
        }

        # 轉換查詢為小寫
        query_lower = query.lower()

        # 檢查是否包含特定關鍵字
        for prompt_type, keywords in keyword_mapping.items():
            if any(keyword in query_lower for keyword in keywords):
                return f"{prompt_type}_guidance"

        return "general_inquiry"


class CollegeRAG:
    def __init__(self, csv_path='college_details_detailed.csv'):
        """
        初始化 RAG 系統，載入大學學群資料並建立嵌入模型，增加錯誤處理
        """
        logger.info("正在初始化CollegeRAG系統")

        try:
            # 確認資料是否存在，不存在則執行爬蟲
            if not os.path.exists(csv_path):
                logger.warning("未找到大學學群資料，正在執行爬蟲...")
                self._scrape_college_data()

            # 載入資料
            self.df = pd.read_csv(csv_path, encoding='utf-8-sig')
            logger.info(f"成功載入 {len(self.df)} 筆大學學群資料")

            # 初始化模型
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"使用設備: {self.device}")

            self.tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
            self.model = AutoModel.from_pretrained(
                "bert-base-chinese").to(self.device)

            # 預計算嵌入
            self.embeddings = self._compute_embeddings()

        except Exception as e:
            logger.error(f"初始化CollegeRAG系統時發生錯誤: {str(e)}")
            raise

    def _scrape_college_data(self):
        """執行爬蟲操作，記錄日誌"""
        try:
            from college import scrape_all_college_details
            scrape_all_college_details()
            logger.info("成功執行大學學群資料爬蟲")
        except Exception as e:
            logger.error(f"爬蟲作業失敗: {str(e)}")
            raise

    def _mean_pooling(self, model_output, attention_mask):
        """均值池化生成句子嵌入"""
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(
            -1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(
            token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def _compute_embeddings(self, batch_size: int = 16) -> np.ndarray:
        """計算所有學群描述的向量嵌入"""
        logger.info("開始計算學群嵌入向量")

        # 組合搜索文本
        search_texts = self.df.apply(
            lambda row: f"{row.get('group_name', '')} {row.get('introduction', '')} {row.get('learning_content', '')} {row.get('related_groups', '')} {row.get('link', '')}",
            axis=1
        )

        embeddings = []

        for i in range(0, len(search_texts), batch_size):
            batch_texts = search_texts[i:i+batch_size].tolist()
            inputs = self.tokenizer(
                batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            batch_embeddings = self._mean_pooling(
                outputs, inputs['attention_mask'])
            embeddings.extend(batch_embeddings.cpu().numpy())

        logger.info(f"完成 {len(embeddings)} 個學群的嵌入向量計算")
        return np.array(embeddings)

    def retrieve_top_k_groups(self, query: str, k: int = 3) -> List[Dict]:
        """根據查詢返回最相關的 k 個學群，增加日誌和錯誤處理"""
        start_time = datetime.now()
        logger.info(f"開始檢索查詢: {query}")

        try:
            inputs = self.tokenizer(query, return_tensors="pt", padding=True,
                                    truncation=True, max_length=512).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            query_embedding = self._mean_pooling(
                outputs, inputs['attention_mask']).cpu().numpy().squeeze()

            similarities = cosine_similarity(
                [query_embedding], self.embeddings)[0]
            top_indices = similarities.argsort()[::-1][:k]

            results = [
                {
                    "group_name": self.df.iloc[idx]['group_name'],
                    "introduction": self.df.iloc[idx]['introduction'],
                    "learning_content": self.df.iloc[idx]['learning_content'],
                    "related_groups": self.df.iloc[idx].get('related_groups', ''),
                    "link": self.df.iloc[idx]['link'],
                    "similarity_score": similarities[idx]
                }
                for idx in top_indices
            ]

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"檢索完成，耗時 {duration} 秒，找到 {len(results)} 個相關學群")

            self._log_retrieval(query, results)
            return results

        except Exception as e:
            logger.error(f"學群檢索時發生錯誤: {str(e)}")
            raise

    def _log_retrieval(self, query: str, results: List[Dict]):
        """記錄檢索日誌到JSONL文件"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "results": [r["group_name"] for r in results]
            }

            with open("retrieval_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"記錄檢索日誌時發生錯誤: {str(e)}")


class BertRAGAgent:
    def __init__(self):
        logger.info("初始化BertRAGAgent")
        self.rag_system = CollegeRAG()

    async def college_rag_search(self, request: RAGRequest):
        """客製化的繁體中文學群搜尋服務，增加錯誤處理和日誌"""
        start_time = datetime.now()
        logger.info(f"收到學群搜尋請求: {request.query}")

        try:
            # 取得相關學群資訊
            top_groups = self.rag_system.retrieve_top_k_groups(request.query)
            context = self.generate_context(request.query, top_groups)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"學群搜尋完成，耗時 {duration} 秒")

            return {
                "查詢內容": request.query,
                "檢索結果": context,
                "推薦學群": top_groups
            }
        except Exception as e:
            logger.error(f"學群搜尋作業發生異常: {str(e)}")
            raise HTTPException(status_code=500, detail=f"學群搜尋作業發生異常：{str(e)}")

    def generate_context(self, query: str, top_groups: List[Dict]) -> str:
        """
        使用 PromptTemplate 生成更智能的上下文
        """
        # 智能推薦提示類型
        prompt_type = PromptTemplate.suggest_prompt_type(query)

        # 使用增強的上下文生成方法
        return PromptTemplate.generate_enhanced_context(query, top_groups, prompt_type)
