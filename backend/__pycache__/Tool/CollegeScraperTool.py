import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict, Union


class CollegeScraperTool:
    def __init__(self):
        self.base_url = "https://collego.edu.tw/Highschool/CollegeList"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def scrape_college_list(self) -> List[Dict[str, str]]:
        """
        爬取 ColleGo 網站的學群列表，取得學群名稱及對應的連結。

        回傳:
            包含學群名稱和連結的列表
        """
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            groups = soup.find_all(
                'a', class_='section__content-item mx-md-6 mx-0')

            if not groups:
                return []

            college_groups = []
            for group in groups:
                label = group.find('label', class_='section__content-label')
                college_groups.append({
                    'group_name': label.text.strip() if label else "未知學群",
                    'link': f"https://collego.edu.tw{group['href']}" if 'href' in group.attrs else "無連結"
                })

            return college_groups

        except requests.RequestException as e:
            print(f"網路請求錯誤: {e}")
            return []

    def scrape_college_details(self, url: str) -> Dict[str, Union[str, List[str]]]:
        """
        抓取單個學群的詳細資訊。

        參數:
            url: 學群詳細頁面的 URL

        回傳:
            包含學群詳細資訊的字典
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            details = {}

            # 學群名稱
            group_name = soup.find(style="font-size:22pt")
            details['group_name'] = group_name.text.strip(
            ) if group_name else "無法抓取學群名稱"

            # 簡介
            intro = soup.find('dd', class_='col-md-10')
            details['introduction'] = intro.text.strip() if intro else "無簡介"

            # 學習內容
            learning_section = soup.find_all('dl', class_='row')
            details['learning_content'] = "\n".join(
                [dd.text.strip()
                 for section in learning_section for dd in section.find_all('dd')]
            ) if learning_section else "無學習內容"

            # 相關學群
            related_groups = soup.find_all('a', style="color:black")
            details['related_groups'] = [link.text.strip()
                                         for link in related_groups] if related_groups else []

            # 主要學科
            main_subjects = soup.find('p', style="font-size:1.2em;")
            details['main_subjects'] = main_subjects.text.strip(
            ) if main_subjects else "無主要學科"

            # 推薦科目
            recommended_subjects_section = soup.find(
                'div', class_='col-xs-12 col-md-10')
            details['recommended_subjects'] = recommended_subjects_section.text.strip(
            ) if recommended_subjects_section else "無推薦科目"

            # 學群內關聯圖表描述
            chart_section = soup.find('div', class_='chart-section')
            details['chart_description'] = chart_section.text.strip(
            ) if chart_section else "無圖表描述"

            return details

        except Exception as e:
            print(f"抓取 URL {url} 時發生錯誤: {e}")
            return {
                "group_name": "抓取失敗",
                "introduction": "抓取失敗",
                "learning_content": "抓取失敗",
                "related_groups": [],
                "main_subjects": "抓取失敗",
                "recommended_subjects": "抓取失敗",
                "chart_description": "抓取失敗"
            }

    def scrape_all_college_details(self) -> List[Dict[str, Union[str, List[str]]]]:
        """
        首先爬取學群列表，接著針對每個學群的連結進一步抓取詳細資訊。

        回傳:
            包含所有學群詳細資訊的列表
        """
        college_groups = self.scrape_college_list()

        if not college_groups:
            print("未能成功抓取學群列表")
            return []

        all_details = []
        for idx, group in enumerate(college_groups, 1):
            print(f"正在抓取學群 {idx}/{len(college_groups)}: {group['group_name']}")
            details = self.scrape_college_details(group['link'])
            details['link'] = group['link']  # 添加學群連結
            all_details.append(details)

            # 延遲避免過快請求
            time.sleep(2)

        # 保存為 CSV
        print("所有學群詳細資訊已抓取完畢，正在保存資料...")
        df = pd.DataFrame(all_details)
        df.to_csv('college_details_detailed.csv',
                  index=False, encoding='utf-8-sig')
        print("資料已成功保存到 college_details_detailed.csv")

        return all_details


# 示例使用
if __name__ == "__main__":
    scraper = CollegeScraperTool()
    results = scraper.scrape_all_college_details()
    if results:
        print(f"成功抓取 {len(results)} 個學群的詳細資訊")
    else:
        print("未抓取到任何學群詳細資訊")
