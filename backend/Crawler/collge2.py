import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict


def scrape_college_list(base_url: str) -> List[Dict]:
    """
    爬取學群列表，取得學群名稱及其詳細頁面的連結。

    回傳:
        包含學群名稱和連結的列表
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    try:
        print(f"正在訪問 {base_url}")
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 抓取學群連結與名稱
        groups = soup.find_all(
            'a', class_='section__content-item mx-md-6 mx-0')
        if not groups:
            print("未找到學群，請檢查網頁結構是否變更")
            return []

        college_groups = []
        for group in groups:
            group_name = group.get_text(strip=True)
            link = f"https://collego.edu.tw{group['href']}" if 'href' in group.attrs else None
            if link:
                college_groups.append({'group_name': group_name, 'link': link})

        print(f"成功提取 {len(college_groups)} 個學群資訊")
        return college_groups

    except Exception as e:
        print(f"爬取學群列表時發生錯誤: {e}")
        return []


def scrape_college_details(group: Dict, headers: Dict) -> Dict:
    """
    爬取單個學群的詳細資訊。

    參數:
        group: 學群名稱及其詳細頁面的連結
        headers: HTTP 請求頭

    回傳:
        包含學群詳細資訊的字典
    """
    url = group['link']
    print(f"正在抓取學群內容: {group['group_name']} ({url})")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 抓取學群主要內容
        details = {
            'group_name': group['group_name'],
            'link': url,
            'introduction': soup.find('div', class_='college-intro').get_text(strip=True) if soup.find('div', class_='college-intro') else "無學群介紹",
            'features': soup.find('div', class_='college-features').get_text(strip=True) if soup.find('div', class_='college-features') else "無特色介紹",
            'related_fields': [field.get_text(strip=True) for field in soup.find_all('li', class_='related-field')] if soup.find_all('li', class_='related-field') else [],
        }

        # 抓取學群內部連結（如進一步介紹頁面）
        sub_links = soup.find_all('a', href=True)
        details['sub_links'] = [
            f"https://collego.edu.tw{link['href']}" for link in sub_links if '/CollegeIntro' in link['href']]

        return details

    except Exception as e:
        print(f"抓取學群內容時發生錯誤: {e}")
        return {
            'group_name': group['group_name'],
            'link': url,
            'introduction': "抓取失敗",
            'features': "抓取失敗",
            'related_fields': [],
            'sub_links': []
        }


def scrape_sub_content(url: str, headers: Dict) -> Dict:
    """
    爬取學群內部子頁面的內容。

    參數:
        url: 子頁面 URL
        headers: HTTP 請求頭

    回傳:
        子頁面的內容字典
    """
    print(f"正在抓取子頁面內容: {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假設子頁面的主要內容在某些特定標籤中
        content = soup.find('div', class_='content-section').get_text(
            strip=True) if soup.find('div', class_='content-section') else "無內容"
        return {'url': url, 'content': content}

    except Exception as e:
        print(f"抓取子頁面內容時發生錯誤: {e}")
        return {'url': url, 'content': "抓取失敗"}


def scrape_all_college_details(base_url: str) -> List[Dict]:
    """
    主函數，爬取整個學群網站，包括學群列表、學群詳細內容及次級頁面內容。

    回傳:
        包含所有學群詳細資訊與次級內容的列表
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }

    # 第一步：爬取學群列表
    college_groups = scrape_college_list(base_url)
    if not college_groups:
        return []

    all_details = []
    for group in college_groups:
        # 第二步：爬取每個學群的詳細內容
        details = scrape_college_details(group, headers)

        # 第三步：爬取次級頁面的內容
        sub_contents = []
        for sub_link in details.get('sub_links', []):
            sub_content = scrape_sub_content(sub_link, headers)
            sub_contents.append(sub_content)

        details['sub_contents'] = sub_contents
        all_details.append(details)

        # 延遲避免過快請求
        time.sleep(2)

    # 保存為 CSV
    print("所有學群詳細資訊已抓取完畢，正在保存資料...")
    df = pd.DataFrame(all_details)
    df.to_csv('college_details_full.csv', index=False, encoding='utf-8-sig')
    print("資料已成功保存到 college_details_full.csv")

    return all_details


if __name__ == "__main__":
    base_url = "https://collego.edu.tw/Highschool/CollegeList"
    results = scrape_all_college_details(base_url)
    if results:
        print(f"成功抓取 {len(results)} 個學群的完整資訊與次級內容")
    else:
        print("未抓取到任何資料")
