NAKHON_PATHOM_ZONING = {
    "กำแพงแสน": "green",
    "เมืองนครปฐม": "red",
    "สามพราน": "purple",
    "พุทธมณฑล": "yellow"
}

def get_zone(location_text: str) -> str:
    if not isinstance(location_text, str):
        return "unknown"
    for area, zone in NAKHON_PATHOM_ZONING.items():
        if area in location_text:
            return zone
    return "unknown"

def check_zoning_compliance(location_text: str, property_type: str) -> bool:
    """เช็คว่า Property Type นั้นสร้างหรือใช้งานตามผังเมืองได้หรือไม่"""
    zone = get_zone(location_text)
  
    if zone == "green" and property_type == "คอนโด":
        return False
    return True

def get_zoning_score(location_text: str, property_type: str) -> int:
    """ให้คะแนนความน่าลงทุน (0-10) เพื่อใช้ในการจัดอันดับทางเลือก"""
    zone = get_zone(location_text)
    if not check_zoning_compliance(location_text, property_type):
        return 0
   
    scores = {
        "red": { # พาณิชยกรรม (เน้นกำไร/หนาแน่น)
            "คอนโด": 10,
            "อาคารพาณิชย์": 9,
            "อพาร์ทเม้นท์": 8,
            "ทาวน์เฮาส์": 6,
            "บ้านเดี่ยว": 4, # ที่ดินแพงเกินไปสำหรับบ้านเดี่ยว
            "ที่ดิน": 7
        },
        "purple": { # อุตสาหกรรม (เน้นการผลิต/คลังสินค้า)
            "โรงงาน": 10,
            "ที่ดิน": 8,
            "อื่นๆ": 7, 
            "บ้านเดี่ยว": 2 # ไม่แนะนำให้นอนเฝ้าโรงงานเพราะมลพิษ
        },
        "yellow": { # ที่อยู่อาศัย (เน้นความสงบ/อยู่อาศัย)
            "บ้านเดี่ยว": 9,
            "ทาวน์เฮาส์": 8,
            "อพาร์ทเม้นท์": 7,
            "คอนโด": 6, # มักถูกจำกัดความสูง
            "ที่ดิน": 7
        },
        "green": { # เกษตรกรรม (เน้นอนุรักษ์/พื้นที่กว้าง)
            "ที่ดิน": 9,
            "บ้านเดี่ยว": 7,
            "อื่นๆ": 5
        }
    }

    # ดึงคะแนนจาก Matrix (ถ้าไม่มีใน List ให้ค่าพื้นฐานที่ 5)
    zone_scores = scores.get(zone, {})
    final_score = zone_scores.get(property_type, 5)
    
    return final_score
   