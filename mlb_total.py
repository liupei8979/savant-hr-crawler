import os
import pandas as pd
import json

# 모든 데이터가 저장된 기본 디렉토리 설정
base_dir = "baseball_data"

# MLB 구장 환경 데이터 읽기
ballpark_file = os.path.join(base_dir, "MLB_Ballpark_Environment_2024.csv")
ballpark_df = pd.read_csv(ballpark_file)

# 통합된 데이터를 저장할 새 구조 생성
combined_data = []

# 구장 데이터의 각 팀 처리
for index, row in ballpark_df.iterrows():
    team_code = str(row["Team"])
    
    # 구장 데이터로 기본 항목 생성
    team_entry = row.to_dict()
    
    # 팀 폴더 찾기
    team_folder = None
    
    # 폴더 구조에서 OAK는 ATH로 사용됨
    if team_code == "OAK":
        team_folder = "ATH"
    else:
        team_folder = team_code
    
    team_dir = os.path.join(base_dir, str(team_folder))
    
    # 팀 디렉토리가 존재하는지 확인
    if os.path.isdir(team_dir):
        # 팀의 통합 CSV 파일 경로 구성
        combined_file = os.path.join(team_dir, f"{team_folder}_combined.csv")
        
        # 통합 파일이 존재하는지 확인
        if os.path.isfile(combined_file):
            try:
                # 팀의 통합 데이터 읽기
                team_data_df = pd.read_csv(combined_file)
                
                # 팀 데이터를 중첩 사전 형식으로 변환
                team_data = team_data_df.to_dict(orient="records")
                
                # 팀 데이터를 중첩된 "TeamData" 필드로 추가
                team_entry["TeamData"] = team_data
                
                print(f"{team_code} ({team_folder}) 데이터를 성공적으로 추가했습니다")
            except Exception as e:
                print(f"{team_code} 처리 중 오류 발생: {str(e)}")
                team_entry["TeamData"] = []
        else:
            print(f"{team_code} ({team_folder})의 통합 파일을 찾을 수 없습니다")
            team_entry["TeamData"] = []
    else:
        print(f"{team_code}의 팀 디렉토리를 찾을 수 없습니다")
        team_entry["TeamData"] = []
    
    # 결과 목록에 통합된 항목 추가
    combined_data.append(team_entry)

# 통합된 데이터를 새 JSON 파일에 저장 (CSV는 중첩 구조를 잘 처리하지 못함)
output_file = os.path.join(base_dir, "MLB_Ballpark_With_TeamData.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(combined_data, f, indent=2)

print(f"통합 데이터가 {output_file}에 저장되었습니다")

# 필요한 경우 평면화된 CSV 버전도 저장
try:
    # 평면화된 레코드를 저장할 빈 목록으로 시작
    flattened_data = []
    
    # 각 팀 처리
    for team_entry in combined_data:
        # 팀 데이터 가져오기
        team_data = team_entry.pop("TeamData", [])
        
        # 팀 데이터가 없으면 구장 정보만 추가
        if not team_data:
            flattened_data.append(team_entry)
        else:
            # 팀 데이터의 각 선수/레코드에 대해
            for record in team_data:
                # 구장 및 선수 데이터를 결합한 새 항목 생성
                combined_record = team_entry.copy()  # 구장 데이터 복사
                
                # 열 이름 충돌을 피하기 위해 팀 데이터 키에 접두사 추가
                for key, value in record.items():
                    combined_record[f"Player_{key}"] = value
                
                flattened_data.append(combined_record)
    
    # DataFrame으로 변환하고 CSV로 저장
    flattened_df = pd.DataFrame(flattened_data)
    csv_output_file = os.path.join(base_dir, "MLB_Ballpark_With_TeamData_Flattened.csv")
    flattened_df.to_csv(csv_output_file, index=False)
    print(f"평면화된 데이터가 {csv_output_file}에 저장되었습니다")
except Exception as e:
    print(f"평면화된 CSV 생성 중 오류 발생: {str(e)}")