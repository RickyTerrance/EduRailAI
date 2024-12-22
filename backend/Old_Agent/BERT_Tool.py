import re
import requests
import os
import torch
import logging
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import json
import time
from typing import List, Dict

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/bert_tool.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def scrape_college_list(url: str = "https://collego.edu.tw/Highschool/CollegeList") -> List[Dict]:
    """爬取ColleGo網站的學群列表"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        logger.info(f"正在訪問 {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        groups = soup.find_all(
            'a', class_='section__content-item mx-md-6 mx-0')

        if not groups:
            logger.warning("未找到任何學群資料")
            return []

        college_groups = []
        for group in groups:
            group_info = {}
            label = group.find('label', class_='section__content-label')
            group_info['group_name'] = label.text.strip() if label else "未知學群"
            group_info['link'] = f"https://collego.edu.tw{group['href']}" if 'href' in group.attrs else "無連結"
            college_groups.append(group_info)

        logger.info(f"成功提取 {len(college_groups)} 個學群資訊")
        return college_groups

    except Exception as e:
        logger.error(f"爬取學群列表時發生錯誤: {e}")
        return []


def scrape_college_details(url: str, headers: Dict) -> Dict:
    """爬取單個學群的詳細資訊"""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        details = {}

        # 提取各項資訊
        group_name = soup.find(style="font-size:22pt")
        details['group_name'] = group_name.text.strip(
        ) if group_name else "無法抓取學群名稱"

        intro = soup.find('dd', class_='col-md-10')
        details['introduction'] = intro.text.strip() if intro else "無簡介"

        learning_section = soup.find_all('dl', class_='row')
        details['learning_content'] = "\n".join([dd.text.strip(
        ) for section in learning_section for dd in section.find_all('dd')]) if learning_section else "無學習內容"

        # 其他欄位也類似處理...

        return details

    except Exception as e:
        logger.error(f"爬取學群詳細資訊時發生錯誤: {str(e)}")
        return {
            "group_name": "抓取失敗",
            "introduction": "抓取失敗",
            "learning_content": "抓取失敗",
            "related_groups": "抓取失敗",
            "compare_subjects": "抓取失敗",
            "important_subjects": "抓取失敗",
            "chart_description": "抓取失敗"
        }


def update_college_data():
    """更新學群資料"""
    try:
        college_groups = scrape_college_list()
        if not college_groups:
            return False

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

        all_details = []
        for group in college_groups:
            details = scrape_college_details(group['link'], headers)
            details['link'] = group['link']
            all_details.append(details)
            time.sleep(2)

        df = pd.DataFrame(all_details)
        df.to_csv('college_details_ALL.csv', index=False, encoding='utf-8-sig')
        return True

    except Exception as e:
        logger.error(f"更新學群資料時發生錯誤: {str(e)}")
        return False


class PromptTemplate:
    """提示模板管理類別"""
    # [保持原有PromptTemplate類別的實作]
    pass


class CollegeRAG:
    """學群RAG系統"""
    # [保持原有CollegeRAG類別的實作]
    pass


def run(query: str, update_data: bool = False) -> Dict:
    """
    Ollama工具入口函數

    參數:
        query: 查詢字串
        update_data: 是否更新資料
    """
    try:
        if update_data:
            logger.info("開始更新學群資料")
            if update_college_data():
                logger.info("學群資料更新成功")
            else:
                logger.warning("學群資料更新失敗，使用現有資料")

        csv_path = 'D:/重要資料/課堂/大四/上/教育數據競賽相關資料/中部五校聯合教育大數據/EduRailAI/backend/college_details_ALL.csv'
        rag_system = CollegeRAG(csv_path=csv_path)
        top_groups = rag_system.retrieve_top_k_groups(query)
        prompt_type = PromptTemplate.suggest_prompt_type(query)
        context = PromptTemplate.generate_enhanced_context(
            query, top_groups, prompt_type)

        return {
            "查詢內容": query,
            "檢索結果": context,
            "推薦學群": top_groups
        }
    except Exception as e:
        logger.error(f"執行BERT工具時發生錯誤: {str(e)}")
        return {
            "error": f"發生錯誤: {str(e)}"
        }
