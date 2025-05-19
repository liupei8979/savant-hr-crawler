# MLB 야구 데이터 처리 파이프라인

## 개요

이 프로젝트는 MLB Baseball Savant 웹사이트에서 홈런 데이터를 수집하고 처리하는 완전한 파이프라인을 제공합니다. 30개 MLB 구장의 홈런 통계를 수집하여 구장 환경 데이터와 통합합니다.

## 기능

- **데이터 수집**: Baseball Savant에서 30개 MLB 구장별 홈런 데이터 자동 수집
- **데이터 통합**: 각 팀별 CSV 파일을 하나의 통합 파일로 결합
- **데이터 병합**: 구장 환경 데이터와 팀별 홈런 데이터를 결합하여 분석용 데이터셋 생성
- **다양한 출력 형식**: JSON(중첩 구조) 및 CSV(평면화된 구조) 형식으로 데이터 제공

## 요구사항

- Python 3.6 이상
- Python 패키지:
  - selenium
  - webdriver-manager
  - pandas
- Chrome 브라우저

## 설치 방법

1. 저장소 클론:

```

git clone https://github.com/liupei8979/mlb-data-pipeline.git
cd mlb-data-pipeline

```

2. 가상 환경 설정(권장):

```

python -m venv venv
source venv/bin/activate # 윈도우의 경우: venv\Scripts\activate

```

3. 필요한 패키지 설치:

```

pip install -r requirements.txt

```

## 의존성 패키지

본 프로젝트는 다음 패키지에 의존합니다 (requirements.txt):

- numpy==2.2.6
- pandas==2.2.3
- python-dateutil==2.9.0.post0
- pytz==2025.2
- six==1.17.0
- tzdata==2025.2

데이터 크롤링을 위해 추가로 필요한 패키지:

```

pip install selenium webdriver-manager

```

이 업데이트를 통해:

1. 기존 설치 방법을 requirements.txt 파일을 사용하는 방식으로 변경했습니다.
2. 프로젝트의 의존성 패키지 목록을 추가했습니다.
3. 크롤링에 필요한 추가 패키지도 설치할 수 있도록 명시했습니다.

requirements.txt 파일에 selenium과 webdriver-manager 패키지가 빠져 있는 것으로 보이므로, 필요하다면 다음 명령어로 requirements.txt 파일을 다시 생성하는 것이 좋습니다:

```

pip install selenium webdriver-manager
pip freeze > requirements.txt

```

## 사용 방법

전체 파이프라인은 세 가지 주요 스크립트로 구성됩니다:

### 1. 데이터 수집 (mlb_statcast_crawler.py)

Baseball Savant에서 각 구장별 홈런 데이터를 수집합니다:

```

python mlb_statcast_crawler.py

```

이 스크립트는 각 MLB 구장에서 발생한 홈런 데이터를 팀별 폴더에 CSV 형식으로 저장합니다.

### 2. 팀별 데이터 통합 (mlb_merge.py)

각 팀 폴더 내의 개별 CSV 파일들을 하나의 통합 파일로 결합합니다:

```

python mlb_merge.py

```

이 스크립트는 각 팀 폴더 내에 `[TEAM_CODE]_combined.csv` 형식으로 통합 파일을 생성합니다.

### 3. 구장 환경 데이터와 통합 (mlb_total.py)

MLB 구장 환경 데이터와 팀별 홈런 데이터를 결합합니다:

```

python mlb_total.py

```

이 스크립트는 다음 두 가지 형식으로 최종 데이터를 생성합니다:

- `MLB_Ballpark_With_TeamData.json`: 중첩 구조의 JSON 파일
- `MLB_Ballpark_With_TeamData_Flattened.csv`: 평면화된 CSV 파일

## 데이터 구조

### 입력 데이터

- `MLB_Ballpark_Environment_2024.csv`: 각 MLB 구장의 환경 정보(거리, 벽 높이, 온도 등)
- 팀별 폴더 내 홈런 데이터 CSV 파일들

### 중간 출력

- 각 팀 폴더 내 `[TEAM_CODE]_combined.csv`: 팀별로 통합된 홈런 데이터

### 최종 출력

- `MLB_Ballpark_With_TeamData.json`: 구장 데이터와 팀별 홈런 데이터가 중첩 구조로 결합된 JSON 파일
- `MLB_Ballpark_With_TeamData_Flattened.csv`: 구장 데이터와 팀별 홈런 데이터가 평면화된 CSV 파일

## 데이터셋 스키마

### JSON 구조

```json
[
  {
    "Team": "팀 코드",
    "Ballpark": "구장 이름",
    "LF_Distance_ft": 좌측 펜스 거리,
    ...기타 구장 환경 속성들...,
    "TeamData": [
      {
        "pitch_type": "투구 타입",
        "game_date": "경기 날짜",
        "release_speed": 투구 속도,
        ...기타 선수/홈런 관련 속성들...
      },
      ... 추가 홈런 기록들 ...
    ]
  },
  ... 다른 팀들에 대한 객체들 ...
]
```

### 주의사항

- 크롤링은 웹사이트의 변경에 따라 작동하지 않을 수 있습니다.
- 대량의 데이터 처리로 인해 시간이 오래 걸릴 수 있습니다.
- 팀 코드와 폴더 이름 불일치에 주의하세요 (예: OAK → ATH).
