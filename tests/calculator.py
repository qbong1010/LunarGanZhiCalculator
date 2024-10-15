import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

class SajuCalculator:
    def __init__(self, service_key):
        self.service_key = service_key
        self.base_url = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getLunCalInfo"
        self.heavenly_stems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
        self.earthly_branches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

    def get_lunar_date(self, solar_date):
        # solYear, solMonth, solDay 추출
        solYear = solar_date.year
        solMonth = f"{solar_date.month:02d}"  # 두 자리로 포맷
        solDay = f"{solar_date.day:02d}"      # 두 자리로 포맷
        
        # REST URL 생성
        response = requests.get(f"{self.base_url}?solYear={solYear}&solMonth={solMonth}&solDay={solDay}&ServiceKey={self.service_key}")
        if response.status_code != 200:
            raise Exception(f"Error: 오류가 발생했습니다. status code {response.status_code}")
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        if items:
            lunar_year = int(items[0].find('lunYear').text)
            lunar_month = int(items[0].find('lunMonth').text)
            lunar_day = int(items[0].find('lunDay').text)
            return lunar_year, lunar_month, lunar_day
        return None

    def calculate_year_stem_branch(self, year):
        stem_index = (year - 4) % 10
        branch_index = (year - 4) % 12
        return self.heavenly_stems[stem_index], self.earthly_branches[branch_index]

    def calculate_month_stem_branch(self, year, month):
        stem_index = (year * 12 + month + 3) % 10
        branch_index = (month + 1) % 12
        return self.heavenly_stems[stem_index], self.earthly_branches[branch_index]

    def calculate_day_stem_branch(self, solar_date):
        # 1900년 1월 1일을 기준으로 날짜 차이를 계산
        base_date = datetime(1900, 1, 1)
        days_passed = (solar_date - base_date).days
        stem_index = days_passed % 10
        branch_index = days_passed % 12
        return self.heavenly_stems[stem_index], self.earthly_branches[branch_index]

    def calculate_hour_stem_branch(self, day_stem, hour):
        day_stem_index = self.heavenly_stems.index(day_stem)
        stem_index = (day_stem_index * 2 + hour // 2) % 10
        branch_index = hour // 2 % 12
        return self.heavenly_stems[stem_index], self.earthly_branches[branch_index]

    def calculate_saju(self, solar_date, hour):
        lunar_date = self.get_lunar_date(solar_date)
        if not lunar_date:
            return None

        year_stem, year_branch = self.calculate_year_stem_branch(lunar_date[0])
        month_stem, month_branch = self.calculate_month_stem_branch(lunar_date[0], lunar_date[1])
        day_stem, day_branch = self.calculate_day_stem_branch(solar_date)
        hour_stem, hour_branch = self.calculate_hour_stem_branch(day_stem, hour)

        return {
            'year': (year_stem, year_branch),
            'month': (month_stem, month_branch),
            'day': (day_stem, day_branch),
            'hour': (hour_stem, hour_branch)
        }

# 사용 예시
if __name__ == "__main__":
    load_dotenv()  # .env 파일에서 환경 변수 로드
    service_key = os.getenv("API_KEY")  # 환경 변수에서 서비스 키 가져오기
    calculator = SajuCalculator(service_key)
    
    # 양력일자를 solYear, solMonth, solDay 형태로 입력받기
    birth_date = datetime(1990, 5, 15)  # 예: 1990년 5월 15일
    birth_hour = 14  # 예: 14시 (오후 2시)
    
    saju = calculator.calculate_saju(birth_date, birth_hour)
    if saju:
        print(f"{response.content}")
        #print(f"년주: {saju['year'][0]}{saju['year'][1]}")
        #print(f"월주: {saju['month'][0]}{saju['month'][1]}")
        #print(f"일주: {saju['day'][0]}{saju['day'][1]}")
        #print(f"시주: {saju['hour'][0]}{saju['hour'][1]}")
    else:
        print("사주 계산에 실패했습니다.")
