# knowledge_base/__init__.py

# ดึงฟังก์ชันที่จำเป็นขึ้นมาให้เรียกใช้ได้ง่ายๆ เมื่อมีการ import knowledge_base
from .city_plan_rules import check_city_plan_risk, get_location_zone
import json
import os

# โหลดไฟล์กฎผู้เชี่ยวชาญ (expert_rules.json) เก็บไว้เป็นตัวแปรตอนเริ่มระบบ
def load_expert_rules():
    file_path = os.path.join(os.path.dirname(__file__), 'expert_rules.json') 
    with open(file_path, 'r', encoding='utf-8') as f:
         return json.load(f)

EXPERT_RULES = load_expert_rules()