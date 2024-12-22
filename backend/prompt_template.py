"""
提示詞模板管理
處理不同類型問題的提示詞生成與管理
"""
import logging
from typing import Dict, Optional, List
from pathlib import Path
import json

# 確保日誌目錄存在
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 配置模板日誌
logger = logging.getLogger(__name__)
template_handler = logging.FileHandler(
    "logs/prompt_template.log", encoding='utf-8')
template_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(template_handler)


class PromptTemplate:
    """提示詞模板類別"""

    # 定義不同類型的提示詞模板
    TEMPLATES = {
        "學群介紹": """
        根據以下學群資訊，回答使用者的問題：
        {context}
        
        使用者問題：{query}
        
        請以條列式回答，並確保：
        1. 內容完整且準確
        2. 回答切中要點
        3. 使用繁體中文
        4. 避免冗長贅述
        5. 重點標示關鍵字
        
        回答結構：
        1. 學群基本介紹（2-3點）
        2. 核心特色（2-3點）
        3. 適合人格特質（2-3點）
        4. 未來發展方向（2-3點）
        """,

        "學習內容": """
        以下是相關學群的學習內容資訊：
        {context}
        
        使用者問題：{query}
        
        請提供完整的學習資訊，包含：
        1. 列出主要課程方向
        2. 說明所需能力
        3. 提供學習建議
        4. 補充相關證照資訊
        5. 建議預修科目
        
        回答結構：
        1. 核心必修課程（3-4門）
        2. 進階選修領域（2-3個）
        3. 重要基礎能力（3-4項）
        4. 建議學習路徑
        5. 實用證照建議
        """,

        "職涯發展": """
        根據以下學群的職涯發展資訊：
        {context}
        
        使用者問題：{query}
        
        請提供詳細的職涯分析：
        1. 可能的職業方向
        2. 產業發展趨勢
        3. 所需專業能力
        4. 薪資發展預期
        5. 進修機會
        
        回答結構：
        1. 主要就業領域（3-4個）
        2. 次要發展方向（2-3個）
        3. 產業趨勢分析
        4. 所需關鍵技能（4-5項）
        5. 職涯成長建議
        """,

        "跨領域發展": """
        參考以下跨領域資訊：
        {context}
        
        使用者問題：{query}
        
        請分析跨領域發展機會：
        1. 相關領域連結
        2. 跨域整合方向
        3. 創新發展機會
        4. 所需補充技能
        
        回答結構：
        1. 主要跨域方向（2-3個）
        2. 建議學習路徑
        3. 創新應用案例
        4. 發展機會分析
        """,

        "升學規劃": """
        依據下列升學資訊：
        {context}
        
        使用者問題：{query}
        
        請提供完整升學建議：
        1. 適合科系推薦
        2. 升學管道分析
        3. 準備方向建議
        4. 時程規劃參考
        
        回答結構：
        1. 推薦科系清單（3-4個）
        2. 各升學管道分析
        3. 準備事項建議
        4. 重要時程提醒
        """,

        "實習就業": """
        根據以下實習與就業資訊：
        {context}
        
        使用者問題：{query}
        
        請提供實習就業指引：
        1. 實習機會分析
        2. 求職市場概況
        3. 面試準備建議
        4. 職場發展建議
        
        回答結構：
        1. 實習機會類型
        2. 求職管道建議
        3. 面試準備重點
        4. 職涯規劃建議
        """
    }

    @staticmethod
    def generate_prompt(
        query: str,
        context: str,
        prompt_type: str = "學群介紹",
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        生成完整的提示詞

        參數:
            query: 使用者問題
            context: 相關內容
            prompt_type: 提示詞類型
            custom_instructions: 自定義指示（可選）

        返回:
            完整提示詞字符串
        """
        try:
            logger.info(f"開始生成提示詞，類型: {prompt_type}")

            # 獲取基本模板
            template = PromptTemplate.TEMPLATES.get(
                prompt_type, PromptTemplate.TEMPLATES["學群介紹"])

            # 添加自定義指示
            if custom_instructions:
                template += f"\n\n額外指示：\n{custom_instructions}"

            # 格式化提示詞
            prompt = template.format(context=context, query=query)

            logger.debug(f"生成的提示詞: {prompt}")
            return prompt

        except Exception as e:
            logger.error(f"生成提示詞時發生錯誤: {str(e)}")
            # 返回基本模板作為後備方案
            return PromptTemplate.TEMPLATES["學群介紹"].format(
                context=context, query=query)

    @staticmethod
    def get_available_templates() -> List[str]:
        """
        獲取所有可用的模板類型

        返回:
            模板類型列表
        """
        return list(PromptTemplate.TEMPLATES.keys())

    @staticmethod
    def add_custom_template(
        template_name: str,
        template_content: str,
        overwrite: bool = False
    ) -> bool:
        """
        添加自定義模板

        參數:
            template_name: 模板名稱
            template_content: 模板內容
            overwrite: 是否覆蓋現有模板

        返回:
            是否添加成功
        """
        try:
            if template_name in PromptTemplate.TEMPLATES and not overwrite:
                logger.warning(f"模板 {template_name} 已存在且未設置覆蓋")
                return False

            PromptTemplate.TEMPLATES[template_name] = template_content
            logger.info(f"成功添加自定義模板: {template_name}")
            return True

        except Exception as e:
            logger.error(f"添加自定義模板時發生錯誤: {str(e)}")
            return False
