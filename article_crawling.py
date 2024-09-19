import requests
from bs4 import BeautifulSoup
import pymysql


# MySQL에 연결하는 함수
def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='user',
        password='1234',
        database='mydb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# 데이터베이스에 데이터를 삽입하는 함수
def insert_news_to_db(connection, title, description, reporter, url, date):
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO article (title, description, reporter, article_url, date)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (title, description, reporter, url, date))
        connection.commit()
    except Exception as e:
        print(f"Error inserting into DB: {e}")


# 기사 요약과 기자 이름을 추출하는 함수
def extract_article_details(article_url):
    try:
        # 기사 페이지 요청
        response = requests.get(article_url)
        article_html = response.text

        # BeautifulSoup으로 HTML 파싱
        article_soup = BeautifulSoup(article_html, 'html.parser')

        # meta 태그에서 description 속성 추출
        description_tag = article_soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'] if description_tag else 'No Description'

        # 기자 이름 추출 (dt 태그에서 class가 name인 경우)
        reporter_tag = article_soup.find('dt', class_='name')
        reporter_name = reporter_tag.get_text(strip=True) if reporter_tag else 'No Reporter'

        return description, reporter_name

    except Exception as e:
        return "No Description", "No Reporter"


# 날짜 형식을 YYYYMMdd로 변환하는 함수
def format_date(date_str):
    try:
        # 날짜 문자열이 MM.ddYYYY 형식인 경우 이를 YYYYMMdd로 변환
        month, day, year = date_str[:2], date_str[3:5], date_str[5:]
        return f"{year}{month}{day}"
    except Exception as e:
        return "Invalid Date"


# 메인 크롤링 함수
def main():
    # URL을 요청하여 페이지 내용을 가져옴
    url = "https://www.mk.co.kr/news/society/general/"
    response = requests.get(url)
    html = response.text

    # BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')

    # MySQL 연결
    connection = connect_db()

    # 각 뉴스 항목을 가져옴 (ad_wrap 클래스를 제외)
    news_list = soup.find_all('li', class_='news_node')

    for news in news_list:
        # ad_wrap 클래스가 포함된 li는 제외
        if 'ad_wrap' in news.get('class', []):
            continue

        # 제목 추출
        title_tag = news.find('h3', class_='news_ttl')
        title = title_tag.get_text(strip=True) if title_tag else 'No Title'

        # 날짜 추출 (안전하게 div가 있는지 먼저 확인)
        time_area = news.find('div', class_='time_area')
        if time_area:
            date_tag = time_area.find('span')
            raw_date = date_tag.get_text(strip=True) if date_tag else 'No Date'
            # 날짜 형식 변환
            date = format_date(raw_date)
        else:
            break

        # 각 기사의 URL 추출
        article_url = news.find('a')['href']

        # 기사 요약과 기자 이름 추출
        description, reporter_name = extract_article_details(article_url)

        # 데이터베이스에 저장
        insert_news_to_db(connection, title, description, reporter_name, article_url, date)

        # 출력
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Reporter: {reporter_name}")
        print(f"URL: {article_url}")
        print(f"Date: {date}")
        print('-' * 50)

    # MySQL 연결 닫기
    connection.close()

# 실행
if __name__ == "__main__":
    main()
