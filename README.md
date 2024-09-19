# <p align="center">[WooriFISA - Crontab 활용하기] 

<h1 style="font-size: 25px;"> 👨‍👨‍👧‍👦💻 개발 팀원 <br>
<br>

|<img src="https://avatars.githubusercontent.com/u/98442485?v=4" width="120" height="120"/>|<img src="https://avatars.githubusercontent.com/u/38968449?v=4" width="120" height="120"/>|<img src="https://avatars.githubusercontent.com/u/175371231?v=4" width="120" height="120"/>|
|:-:|:-:|:-:|
|[@최영하](https://github.com/LeeYeonhee-00)|[@허예은](https://github.com/yyyeun)|[@오재웅](https://github.com/ohwoong2)|
<br>

# 🙆‍♀️ 프로젝트 개요 : Article Monitoring System
1. Crontab 자동화로 3시간마다 [뉴스 데이터](https://www.mk.co.kr/news/society/general/)를 크롤링하여 DB에 적재
2. ELK 파이프라인 구축해 Elasticsearch에 전달
<br>

# ⛷ 학습 목적
- Linux에서 Crontab 활용하기
<br>

# 🛠 기술 스택 
- Crawling: Python 3.10
- Database: MySQL 8.0
- Search Engine: ELK Stack 7.11
- Container: Docker Compose
<br>

# 🥾 실행 순서 
1. Docker 설치
```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo systemctl status docker
sudo usermod -aG docker $USER
```

2. Docker Compose 설정 후 실행 (MySQL, ELK)
```
cd /home/username/compose/
sudo apt install docker-compose
docker-compose up -d
```

3. DB 초기 설정
```sql
CREATE TABLE article (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    reporter VARCHAR(100) NOT NULL,
    article_url VARCHAR(255) NOT NULL,
    date DATE NOT NULL
);
```
- DBeaver에서 allowPublicKeyRetrieval: true, useSSL: false 설정
  <img src="https://github.com/user-attachments/assets/3a0837c6-b255-42d6-b693-8123dd141746" width="600" height="400"/>

4. Python 라이브러리 설치 및 크롤링 파일(article_crawling.py) 작성
```
sudo apt update
sudo apt install python3-pip

sudo pip3 install beautifulsoup4
sudo pip3 install pymysql
```

5. Crontab 자동화에 따른 DB 적재
```
0 */3 * * * python3 crawling.py >/dev/null 2>&1
```

6. ELK 파이프라인 실행

7. Postman 테스트
<br>

# 🖼 실행 결과

1. 크롤링 후 DB 적재
<img src="https://github.com/user-attachments/assets/59f799ba-f8cf-427d-866a-ffaa9d58b33c">

<br><br>

# ✨ 트러블슈팅 
```
sudo apt-get update
```
중 오류 발생

<img src="https://github.com/user-attachments/assets/13868a39-fc73-45ed-8748-48781e8b8bf9">
<br><br>

```
sudo apt-get clean 
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get upgrade -y
sudo apt-get update
```
사용으로 해결



