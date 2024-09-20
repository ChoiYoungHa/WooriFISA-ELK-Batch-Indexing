# <p align="center">[💎WooriFISA - SearchEngine Crontab Batch Indexing] 

<h2 style="font-size: 25px;"> 👨‍👨‍👧‍👦💻 개발 팀원 <br>
<br>
    
|<img src="https://avatars.githubusercontent.com/u/64997345?v=4" width="120" height="120"/>|<img src="https://avatars.githubusercontent.com/u/38968449?v=4" width="120" height="120"/>|<img src="https://avatars.githubusercontent.com/u/175371231?v=4" width="120" height="120"/>|<img src="https://avatars.githubusercontent.com/u/82391356?v=4" width="120" height="120"/>
|:-:|:-:|:-:|:-:|
|[@최영하](https://github.com/ChoiYoungha)|[@허예은](https://github.com/yyyeun)|[@오재웅](https://github.com/ohwoong2)|[@이정민](https://github.com/jjeong1015) 



<br>

# 🙆‍♀️ 프로젝트 개요
Crontab이 실제로 많이 활용되는 검색엔진 배치 수집을 구현하고자 했습니다. <br>
데이터 수집을 자동화하며, 이를 인덱싱해 형태소 단위로 해당 기사를 쉽게 검색할 수 있도록 구현했습니다. 

1. Crontab 자동화로 3시간마다 [뉴스 데이터](https://www.mk.co.kr/news/society/general/)를 크롤링하여 Mysql DB에 적재
2. ELK 파이프라인 구축해 Elasticsearch에 전달

<br>

# ⛷ 학습 목적
- Linux에서 Crontab 활용하기
- 검색엔진 배치 수집 후 검색기능 구현하기
<br>

# 🛠 기술 스택 
- Crawling: Python 3.10
- Database: MySQL 8.0
- Search Engine: ELK Stack 7.11.1
- Container: Docker Compose
<br>

# 🥾 실행 순서 
### 1.Docker 설치🎨
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

### 2.Docker Compose 설정 후 실행 (MySQL, ELK)👌
```
cd /home/username/compose/
sudo apt install docker-compose
docker-compose up -d
```

### 3. Mysql 스키마 생성🎫
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

### 4. Python 라이브러리 설치 및 크롤링 파일(article_crawling.py) 작성🕶
```
sudo apt update
sudo apt install python3-pip

sudo pip3 install beautifulsoup4
sudo pip3 install pymysql
```

### 5. Crontab 자동화에 따른 DB 적재👝
```
0 */3 * * * python3 crawling.py >/dev/null 2>&1
```

### 6. ELK 파이프라인 실행🧶
```
input {
  jdbc {
    jdbc_driver_library => "/usr/share/logstash/mysql-connector-java-8.0.18.jar"
    jdbc_driver_class => "com.mysql.cj.jdbc.Driver"
    jdbc_connection_string => "jdbc:mysql://mysql:3306/mydb"
    jdbc_user => "(user)"
    jdbc_password => "(password)"
    jdbc_validate_connection => true
    schedule => "* * * * *"
    statement => "SELECT title, description, reporter, article_url, date FROM article"
  }
}

filter {
  date {
    match => ["date", "ISO8601"]
    target => "date"
  }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]
    index => "article"
  }

  stdout { 
    codec => rubydebug
  }
}
```

<br>

# 🖼 실행 결과

### 1. 크롤링 후 DB 적재🦞
<img src="https://github.com/user-attachments/assets/59f799ba-f8cf-427d-866a-ffaa9d58b33c">

<br><br>

### 2. Logstash를 사용해 Elasticsearch에 전달🍙
<img src="https://github.com/user-attachments/assets/d7f4b016-e6a4-4031-bc18-8fa3b58f82a1">

<br><br>

### 3. Postman으로 확인🍨
<img src="https://github.com/user-attachments/assets/18fd9bb3-473d-4bce-95b3-9ec2d5c6e03f">

<br><br>

# ✨ 트러블슈팅 
### 1. sudo apt-get update 중 오류 발생🎃

<img src="https://github.com/user-attachments/assets/13868a39-fc73-45ed-8748-48781e8b8bf9">
<br><br>

```
sudo apt-get clean 
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get upgrade -y
sudo apt-get update
```


<br>

### 2. logstash 7.11.1 / mysql 8.0 jdbc driver 호환성 문제🎯

<img src="https://github.com/user-attachments/assets/1d54af95-84de-4807-91fb-07a6f5da0f71">
<br>

- 도커 컨테이너 /usr/share/logstash/ 위치에 mysql jdbc driver 위치시키고, 실행권한 및 소유자까지 변경했는데도 드라이버를 로드할 수 없다는 에러 발생

<br><br>

<img src="https://github.com/user-attachments/assets/df525a38-6f31-47f1-ab13-f3990b46541f">
<br>

- 3개의 드라이버를 테스트해본 결과 8.0.18버전과 호환됨을 확인

<br><br>

### 3. Docker container 종속문제🍿

<img src="https://future-zydeco-6c6.notion.site/image/https%3A%2F%2Fprod-files-secure.s3.us-west-2.amazonaws.com%2Ff22dc327-0788-4704-8c79-3fa8e796e498%2F590116b8-92a3-415a-bcb1-a998a4edf0b2%2F2024-09-19_22_49_33.png?table=block&id=1064abc5-319b-8078-9924-f8f47aee30ae&spaceId=f22dc327-0788-4704-8c79-3fa8e796e498&width=1420&userId=&cache=v2">

```
input {
  jdbc {
    jdbc_driver_library => "/usr/share/logstash/mysql-connector-java-8.0.18.jar"
    jdbc_driver_class => "com.mysql.cj.jdbc.Driver"
    jdbc_connection_string => "jdbc:mysql://mysql:3306/mydb"  # 기존: jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/mydb"
    jdbc_user => "user"
    jdbc_password => "1234"
    jdbc_validate_connection => true
    schedule => "* * * * *"
    statement => "SELECT title, description, reporter, article_url, date FROM article"
  }
}

filter {
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"]  # 기존: hosts => ["http://127.0.0.1:9200"]
    index => "article"
  }

  stdout { 
    codec => rubydebug
  }
}
```

- 기존 yaml 파일 사용 시 DB와 연결할 수 없으며 EK도 찾을 수 없다는 에러 발생
- mysql, elasticsearch는 logstash와 같은 docker compose에 종속된 컨테이너이므로 127.0.0.1은 logstash 자기 자신을 의미
- 때문에 docker compose의 서비스명을 명시해주어야 함
<br>
