import os
import pandas as pd
import glob

# 팀 폴더가 있는 메인 디렉토리
base_dir = "baseball_data"

# 팀 디렉토리 목록 가져오기
team_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

# 각 팀 디렉토리 처리
for team in team_dirs:
    team_path = os.path.join(base_dir, team)
    
    # 팀 디렉토리의 모든 CSV 파일 찾기
    csv_files = glob.glob(os.path.join(team_path, "*.csv"))
    
    # 해당 팀의 모든 DataFrame을 저장할 리스트
    team_dfs = []
    
    # 각 CSV 파일 처리
    for file in csv_files:
        # CSV 파일 읽기
        df = pd.read_csv(file)
        team_dfs.append(df)
        print(f"{file} 처리 완료")
    
    # 해당 팀의 모든 DataFrame 합치기
    if team_dfs:
        combined_df = pd.concat(team_dfs, ignore_index=True)
        
        # 합쳐진 데이터 저장 (팀 폴더 내에)
        output_file = os.path.join(team_path, f"{team}_combined.csv")
        combined_df.to_csv(output_file, index=False)
        print(f"{team} 팀의 통합된 데이터가 {output_file}에 저장되었습니다")
        print(f"{team} 팀의 총 행 수: {len(combined_df)}")
    else:
        print(f"{team} 팀 폴더에서 CSV 파일을 찾을 수 없습니다")