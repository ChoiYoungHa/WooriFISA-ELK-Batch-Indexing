# <p align="center">[FISA3-Crontab] 


<h2 style="font-size: 25px;"> 개발팀원👨‍👨‍👧‍👦💻<br>
<br>

|<img src="https://avatars.githubusercontent.com/u/98442485?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/38968449?v=4" width="150" height="150"/>|<img src="https://avatars.githubusercontent.com/u/175371231?v=4" width="150" height="150"/>|
|:-:|:-:|:-:|
|[@최영하](https://github.com/LeeYeonhee-00)|[@허예은](https://github.com/yyyeun)|[@오재웅](https://github.com/ohwoong2)|
---

<br>

## 학습 목적 ⛷

- Crontab 활용
<br>

## 주요 기능 🚁
- 크롤링 후 DB 데이터 적재
- DB 데이터 Elastic Search 전달
- Crontab 자동화
<br>

## 사용 기술 스택 🛠
- 크롤링: 
- 데이터베이스: MySQL
- 검색 서비스: ELK Stack (Elasticsearch, Logstash, Kibana)
- 컨테이너화: Docker Compose
<br>

## 실행 순서

<br>

## 트러블슈팅

<img src="https://github.com/user-attachments/assets/13868a39-fc73-45ed-8748-48781e8b8bf9">
<br>

```
sudo apt-get update
```
오류 발생 시


```
sudo apt-get clean 
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get upgrade -y
sudo apt-get update
```
사용으로 해결


