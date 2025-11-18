import requests
from bs4 import BeautifulSoup


def get_today_news():
    try:
        url = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return f"뉴스 요청 실패: {response.status_code}"

        soup = BeautifulSoup(response.content, features="xml")
        items = soup.findAll("item")
        if not items:
            return "뉴스 항목이 없습니다."

        headlines = []
        for item in items[:5]:
            title = item.title.text if item.title else "제목 없음"
            headlines.append(title)

        return "\n".join(headlines)
    except Exception as e:
        return f"뉴스를 불러오는 중 오류가 발생했습니다: {e}"
