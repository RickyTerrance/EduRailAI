import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict


def scrape_college_list(url: str = "https://collego.edu.tw/Highschool/CollegeList") -> List[Dict]:
    """
    爬取 ColleGo 網站的學群列表，取得學群名稱及對應的連結。

    回傳:
        包含學群名稱和連結的列表
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    try:
        print(f"正在訪問 {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"HTTP 請求失敗，狀態碼: {response.status_code}")
            return []

        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        groups = soup.find_all(
            'a', class_='section__content-item mx-md-6 mx-0')

        if not groups:
            print("未找到任何學群資料，請確認網站結構是否變更")
            return []

        college_groups = []
        for group in groups:
            group_info = {}

            label = group.find('label', class_='section__content-label')
            group_info['group_name'] = label.text.strip() if label else "未知學群"

            group_info['link'] = f"https://collego.edu.tw{group['href']}" if 'href' in group.attrs else "無連結"

            college_groups.append(group_info)

        print(f"成功提取 {len(college_groups)} 個學群資訊")
        return college_groups

    except requests.RequestException as e:
        print(f"網路請求錯誤: {e}")
        return []
    except Exception as e:
        print(f"未知錯誤: {e}")
        return []


def scrape_college_details(url: str, headers: Dict) -> Dict:
    """
    抓取單個學群的詳細資訊。

    參數:
        url: 學群詳細頁面的 URL
        headers: HTTP 請求頭

    回傳:
        包含學群詳細資訊的字典
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        details = {}

        # 學群名稱
        group_name = soup.find(style="font-size:22pt")
        details['group_name'] = group_name.text.strip(
        ) if group_name else "無法抓取學群名稱"
        print(f"1. 抓取學群名稱: {details['group_name']}")

        # 簡介
        intro = soup.find('dd', class_='col-md-10')
        details['introduction'] = intro.text.strip() if intro else "無簡介"
        print(f"2. 抓取簡介: {details['introduction']}")

        # 學習內容
        learning_section = soup.find_all('dl', class_='row')
        if learning_section:
            learning_content = []
            for section in learning_section:
                dd_items = section.find_all('dd')
                learning_content += [dd.text.strip() for dd in dd_items]
            details['learning_content'] = "\n".join(learning_content)
        else:
            details['learning_content'] = "無學習內容"
        print(f"3. 抓取學習內容: {details['learning_content']}")

        # 抓取所有相關學群
        related_groups_sections = soup.find_all(
            'a',
            style=lambda value: 'font-size:1.3em' in value if value else False,
            target='_blank'
        )
        if related_groups_sections:
            related_groups = []
            for section in related_groups_sections:
                # 提取 <u> 標籤內文字
                u_items = section.find_all('u')
                related_groups.extend([u.text.strip() for u in u_items])

            details['related_groups'] = "\n".join(
                related_groups) if related_groups else "無相關學群"
        else:
            details['related_groups'] = "無相關學群"

        print(f"4. 抓取相關學群: {details['related_groups']}")

        # 比較科目
        compare_subjects = []  # 初始化空陣列
        count_title_items = soup.find_all(
            'h4', class_='count-title')  # 抓取所有 h4 標籤
        if count_title_items:
            for item in count_title_items:
                text = re.sub(r'<.*?>', '', str(item))  # 使用正規表達式去除標籤
                compare_subjects.append(text.strip())  # 移除標籤後的純文字
            details['compare_subjects'] = "\n".join(
                compare_subjects)  # 將陣列轉為字串
        else:
            details['compare_subjects'] = "無比較科目"
        print(f"5. 抓取比較科目: {details['compare_subjects']}")

        # 重點科目
        important_subjects = []  # 初始化空陣列
        nobr_items = soup.find_all('nobr')  # 抓取所有 nobr 標籤
        if nobr_items:
            for item in nobr_items:
                text = re.sub(r'<.*?>', '', str(item))  # 使用正規表達式去除標籤
                important_subjects.append(text.strip())  # 移除標籤後的純文字
            details['important_subjects'] = "\n".join(
                important_subjects)  # 將陣列轉為字串
        else:
            details['important_subjects'] = "無重點科目"
        print(f"6. 抓取重點科目: {details['important_subjects']}")

        # 學群內關聯圖表描述
        chart_section = soup.find('dd', class_='col-md-5')
        chart_description = chart_section.text.strip() if chart_section else "無圖表描述"
        print(f"7. 抓取圖表描述: {chart_description}")

        # 整合更多資訊
        details['compare_contents'] = count_title_items
        details['important_contents'] = nobr_items
        details['chart_description'] = chart_description

        return details

    except Exception as e:
        print(f"抓取 URL {url} 時發生錯誤: {e}")
        return {
            "group_name": "抓取失敗",
            "introduction": "抓取失敗",
            "learning_content": "抓取失敗",
            "related_groups": [],
            "compare_subjects": "抓取失敗",
            "important_subjects": "抓取失敗",
            "chart_description": "抓取失敗"
        }


def scrape_all_college_details() -> List[Dict]:
    """
    首先爬取學群列表，接著針對每個學群的連結進一步抓取詳細資訊。

    回傳:
        包含所有學群詳細資訊的列表
    """
    base_url = "https://collego.edu.tw/Highschool/CollegeList"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    # 第一步：爬取學群列表
    college_groups = scrape_college_list(base_url)

    if not college_groups:
        print("未能成功抓取學群列表")
        return []

    # 第二步：對每個學群抓取詳細資訊
    all_details = []
    for idx, group in enumerate(college_groups, 1):
        print(f"正在抓取學群 {idx}/{len(college_groups)}: {group['group_name']}")
        details = scrape_college_details(group['link'], headers)
        details['link'] = group['link']  # 添加學群連結
        all_details.append(details)

        # 延遲避免過快請求
        time.sleep(2)

    # 保存為 CSV
    print("所有學群詳細資訊已抓取完畢，正在保存資料...")
    df = pd.DataFrame(all_details)
    df.to_csv('college_details_ALL.csv',
              index=False, encoding='utf-8-sig')
    print("資料已成功保存到 college_details_ALL.csv")

    return all_details


if __name__ == "__main__":
    results = scrape_all_college_details()
    if results:
        print(f"成功抓取 {len(results)} 個學群的詳細資訊")
    else:
        print("未抓取到任何學群詳細資訊")
