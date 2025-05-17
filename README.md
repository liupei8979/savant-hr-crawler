```
# MLB Statcast 홈런 데이터 크롤러

## 개요
이 프로젝트는 MLB Baseball Savant 웹사이트에서 각 구장별 홈런 데이터를 자동으로 수집하는 크롤러입니다. 30개 MLB 구장의 홈런 통계를 개별 폴더에 CSV 형식으로 저장합니다.

## 기능
- 30개 MLB 구장별 홈런 데이터 자동 수집
- 팀 코드별 개별 폴더 생성 (예: NYY, LAD 등)
- 각 타자별 홈런 데이터를 CSV 파일로 다운로드
- 오류 발생 시 스크린샷 자동 저장

## 요구사항
- Python 3.6 이상
- 다음 Python 패키지:
  - selenium
  - webdriver-manager
- Chrome 브라우저

## 설치 방법
1. 저장소 클론:
```

git clone https://github.com/[사용자명]/savant-hr-crawler.git
cd savant-hr-crawler

```

2. 필요한 패키지 설치:
```

pip install selenium webdriver-manager

```

## 사용 방법
다음 명령어로 크롤러를 실행합니다:
```

python mlb_statcast_crawler.py

```

## 데이터 구조
크롤러 실행 후, 다음과 같은 폴더 구조가 생성됩니다:
```

baseball_data/
├── NYY/ # 뉴욕 양키스 (Yankee Stadium)
├── LAD/ # LA 다저스 (Dodger Stadium)
├── SD/ # 샌디에고 파드레스 (Petco Park)
└── ... (기타 모든 MLB 구장)

```

각 팀 폴더 내에는 해당 구장에서 홈런을 친 타자들의 CSV 데이터 파일이 저장됩니다.

## 주의사항
- 크롤링은 웹사이트의 변경에 따라 작동하지 않을 수 있습니다.
- 대량의 데이터 다운로드로 인해 시간이 오래 걸릴 수 있습니다.
- 인터넷 연결 상태에 따라 오류가 발생할 수 있습니다.

## 라이선스
[여기에 라이선스 정보 추가]
```
