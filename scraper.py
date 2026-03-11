import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_trending():
    # 伪装成真实的浏览器“受体”
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }
    url = "https://github.com/trending"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        trending_data = []
        
        articles = soup.find_all("article", class_="Box-row")
        
        for article in articles[:5]:
            h2 = article.find("h2", class_="h3 lh-condensed")
            repo_path = h2.a["href"].strip() if h2 and h2.a else "Unknown"
            
            p_desc = article.find("p", class_="col-9 color-fg-muted my-1 pr-4")
            description = p_desc.text.strip() if p_desc else "暂无描述"
            
            stars_today = "0 stars today"
            for span in article.find_all("span", class_="d-inline-block float-sm-right"):
                if "stars today" in span.text:
                    stars_today = span.text.strip()
                    break
            
            trending_data.append({
                "repo": repo_path,
                "description": description,
                "stars_today": stars_today,
                "url": "https://github.com" + repo_path
            })
            
        output = {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "top_5_trending": trending_data
        }
        
        with open("trending.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_trending()
