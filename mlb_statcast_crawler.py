from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil

# 메인 저장 폴더 생성
save_dir = "baseball_data"
os.makedirs(save_dir, exist_ok=True)

# 경기장 ID 목록
venues = [
    {"id": "3313", "name": "NYY - Yankee Stadium"},
    {"id": "22", "name": "LAD - Dodger Stadium"},
    {"id": "2680", "name": "SD - Petco Park"},
    {"id": "3289", "name": "NYM - Citi Field"},
    {"id": "2681", "name": "PHI - Citizens Bank Park"},
    {"id": "3312", "name": "MIN - Target Field"},
    {"id": "2395", "name": "SF - Oracle Park"},
    {"id": "5325", "name": "TEX - Globe Life Field"},
    {"id": "3309", "name": "WSH - Nationals Park"},
    {"id": "2889", "name": "STL - Busch Stadium"},
    {"id": "4705", "name": "ATL - Truist Park"},
    {"id": "680", "name": "SEA - T-Mobile Park"},
    {"id": "4169", "name": "MIA - loanDepot Park"},
    {"id": "2394", "name": "DET - Comerica Park"},
    {"id": "32", "name": "MIL - American Family Field"},
    {"id": "2392", "name": "HOU - Daikin Park"},
    {"id": "15", "name": "AZ - Chase Field"},
    {"id": "31", "name": "PIT - PNC Park"},
    {"id": "2602", "name": "CIN - Great American Ball Park"},
    {"id": "1", "name": "LAA - Angel Stadium"},
    {"id": "3", "name": "BOS - Fenway Park"},
    {"id": "14", "name": "TOR - Rogers Centre"},
    {"id": "19", "name": "COL - Coors Field"},
    {"id": "2", "name": "BAL - Oriole Park"},
    {"id": "7", "name": "KC - Kauffman Stadium"},
    {"id": "17", "name": "CHC - Wrigley Field"},
    {"id": "5", "name": "CLE - Progressive Field"},
    {"id": "4", "name": "CWS - Rate Field"},
    {"id": "12", "name": "TB - Tropicana Field"},
    {"id": "10", "name": "ATH - Oakland Coliseum"}
]

base_url = "https://baseballsavant.mlb.com/statcast_search?hfPT=&hfAB=home%5C.%5C.run%7C&hfGT=R%7C&hfPR=&hfZ=&hfStadium={venue_id}%7C&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=2024%7C&hfSit=&player_type=batter&hfOuts=&hfOpponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt=&game_date_lt=&hfMo=&hfTeam=&home_road=&hfRO=&position=&hfInfield=&hfOutfield=&hfInn=&hfBBT=&hfFlag=&metric_1=&group_by=name&min_pitches=0&min_results=0&min_pas=0&sort_col=pitches&player_event_sort=api_p_release_speed&sort_order=desc#results"

try:
    for venue in venues:
        # 경기장 이름에서 유효한 폴더명 생성 (팀 코드 사용)
        team_code = venue["name"].split(" - ")[0].strip()
        venue_folder = os.path.join(save_dir, team_code)
        
        # 해당 경기장 전용 폴더 생성
        os.makedirs(venue_folder, exist_ok=True)
        
        # 크롬 드라이버 설정 - 각 경기장별 다운로드 폴더 지정
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.abspath(venue_folder),
            "download.prompt_for_download": False,
        })
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        try:
            # 각 경기장 URL 열기
            current_url = base_url.format(venue_id=venue["id"])
            driver.get(current_url)
            print(f"Processing {venue['name']}...")
            
            # 결과 로딩 대기
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#search-results-container tbody tr"))
            )
            
            # 모든 행(tr) 가져오기
            rows = driver.find_elements(By.CSS_SELECTOR, "#search-results-container tbody tr")
            print(f"Found {len(rows)} rows in table")
            
            for i, row in enumerate(rows):
                try:
                    # 모든 셀 가져오기
                    cells = row.find_elements(By.TAG_NAME, "td")
                    
                    if len(cells) >= 7:
                        # 7번째 셀(Graphs)을 찾기
                        graphs_cell = cells[6]  # 인덱스는 0부터 시작하므로 7번째 셀은 인덱스 6
                        
                        # 셀 내용 확인
                        print(f"Row {i+1}, Cell 7 text: {graphs_cell.text}")
                        
                        if "Graphs" in graphs_cell.text:
                            # Graphs 셀을 직접 클릭
                            print(f"Clicking on Graphs cell for row {i+1}")
                            graphs_cell.click()
                            
                            # 차트 옵션이 로드될 때까지 대기
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, ".chart-options"))
                            )
                            
                            # CSV 다운로드 버튼 찾기 및 클릭
                            csv_div = driver.find_element(By.CSS_SELECTOR, ".chart-options .csv")
                            print(f"Found CSV download option: {csv_div.text}")
                            csv_div.click()
                            
                            # 다운로드 시간 대기
                            time.sleep(3)
                            
                            # 차트 닫기 (모달 닫기 버튼)
                            close_btn = driver.find_element(By.CSS_SELECTOR, ".close-modal")
                            close_btn.click()
                            
                            # 다음 작업 전 짧은 대기
                            time.sleep(2)
                            
                            print(f"  Downloaded CSV for row {i+1} to {team_code} folder")
                        else:
                            print(f"No Graphs text in cell 7 for row {i+1}")
                    else:
                        print(f"Row {i+1} does not have enough cells")
                    
                except Exception as e:
                    print(f"  Error processing row {i+1}: {str(e)}")
                    driver.save_screenshot(os.path.join(venue_folder, f"error_row_{i+1}.png"))
            
            print(f"Completed {venue['name']}")
            
        except Exception as e:
            print(f"Error processing venue {venue['name']}: {str(e)}")
            driver.save_screenshot(os.path.join(venue_folder, "error_venue.png"))
        
        finally:
            # 각 경기장 처리 후 드라이버 종료
            driver.quit()

except Exception as e:
    print(f"Main error: {str(e)}")

print("All venues processed")