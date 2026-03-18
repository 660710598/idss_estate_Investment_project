# knowledge_base/city_plan_rules.py

# 1. ฐานข้อมูลผังเมืองจำลอง (Mapping พื้นที่ใน จ.นครปฐม)
# ทำเป็น Dictionary เก็บข้อมูลโซน เพื่อให้นำไปดึงเช็คได้ง่าย
LOCATION_ZONES = {
  # --- โซนสีแดง (พาณิชยกรรม: พุทธมณฑล / ศาลายา) ---
    "ศาลายา": {"color": "Red", "type": "Commercial", "description": "พื้นที่พาณิชยกรรมหนาแน่นสูง ใกล้มหาวิทยาลัย"},
    "พุทธมณฑล": {"color": "Red", "type": "Commercial", "description": "ศูนย์กลางพาณิชยกรรมและบริการ"},
    "สถานีรถไฟศาลายา": {"color": "Red", "type": "Commercial", "description": "พื้นที่รอบสถานีขนส่งมวลชน"},

    # --- โซนสีเหลือง (ที่อยู่อาศัย: เมืองนครปฐม) ---
    "เมืองนครปฐม": {"color": "Yellow", "type": "Medium Density", "description": "ที่อยู่อาศัยหนาแน่นปานกลาง เขตเทศบาล"},
    "นครปฐม": {"color": "Yellow", "type": "Medium Density", "description": "ที่อยู่อาศัยหนาแน่นปานกลาง"},
    "สนามจันทร์": {"color": "Yellow", "type": "Medium Density", "description": "ย่านที่อยู่อาศัยและสถานศึกษา"},
    "ห้วยจรเข้": {"color": "Yellow", "type": "Medium Density", "description": "พื้นที่ขยายตัวของที่อยู่อาศัย"},
    "พระปฐมเจดีย์": {"color": "Yellow", "type": "Medium Density", "description": "พื้นที่ชุมชนเก่าและที่อยู่อาศัย"},
    "นครชัยศรี": {"color": "Yellow", "type": "Medium Density", "description": "ที่อยู่อาศัยแนวราบและชุมชนริมน้ำ"},

    # --- โซนสีม่วง (อุตสาหกรรม: สามพราน / อ้อมใหญ่) ---
    "สามพราน": {"color": "Purple", "type": "Industrial", "description": "เขตอุตสาหกรรมและคลังสินค้าหลัก"},
    "อ้อมใหญ่": {"color": "Purple", "type": "Industrial", "description": "ย่านโรงงานอุตสาหกรรมหนาแน่น"},
    "ไร่ขิง": {"color": "Purple", "type": "Industrial", "description": "พื้นที่อุตสาหกรรมต่อเนื่อง"},
    "กระทุ่มล้ม": {"color": "Purple", "type": "Industrial", "description": "พื้นที่รองรับโรงงานและโกดัง"},

    # --- โซนสีเขียว (เกษตรกรรม: กำแพงแสน / ดอนตูม) ---
    "กำแพงแสน": {"color": "Green", "type": "Agriculture", "description": "พื้นที่เกษตรกรรมและอนุรักษ์ชนบท"},
    "ทุ่งลูกนก": {"color": "Green", "type": "Agriculture", "description": "เขตเกษตรกรรมและฟาร์มเลี้ยงสัตว์"},
    "ดอนตูม": {"color": "Green", "type": "Agriculture", "description": "พื้นที่เกษตรกรรมหลัก"},
    "บางเลน": {"color": "Green", "type": "Agriculture", "description": "พื้นที่เกษตรกรรมและที่ราบลุ่มน้ำ"},
    "ทุ่งกระพังโหม": {"color": "Green", "type": "Agriculture", "description": "เขตเกษตรกรรมหนาแน่นน้อย"},
    "คลองโยง": {"color": "Green", "type": "Agriculture", "description": "พื้นที่เกษตรกรรมและรักษาสภาพแวดล้อม"}
}

def get_location_zone(location_text):
    """
    ฟังก์ชันเช็คโซนสีผังเมือง: 
    รับค่า string เช่น 'ศาลายา, พุทธมณฑล' แล้วเทียบกับฐานข้อมูล
    """
    for key, data in LOCATION_ZONES.items():
        if key in str(location_text):
            return data["color"]
    # ถ้าหาไม่เจอให้ค่าเริ่มต้นเป็นสีเหลือง (ที่อยู่อาศัยทั่วไป)
    return "Yellow"

def check_city_plan_risk(location_text, property_type):
    """
    ฟังก์ชันประเมินความเสี่ยงตามผังเมือง:
    ส่งกลับเป็น List ของความเสี่ยง (Warning messages) ถ้านำไปทำ UI สามารถเอา List นี้ไปโชว์เตือนผู้ใช้ได้เลย
    """
    zone = get_location_zone(location_text)
    risks = []
    
    # กฎข้อที่ 1: พื้นที่สีเขียว (เกษตรกรรม)
    if zone == "Green":
        if property_type in ["คอนโด", "โรงงาน", "ร้านขาย"]:
            risks.append("⚠️ ความเสี่ยงสูง: พื้นที่สีเขียวไม่อนุญาตให้สร้างอาคารสูงหรือโรงงาน")
        if property_type == "ที่ดิน":
            risks.append("✅ ข้อแนะนำ: เหมาะสำหรับทำการเกษตร หรือซื้อเก็งกำไรระยะยาวเท่านั้น")
            
    # กฎข้อที่ 2: พื้นที่สีแดง (พาณิชยกรรม)
    elif zone == "Red":
        if property_type == "บ้านเดี่ยว":
            risks.append("⚠️ ข้อควรระวัง: ราคาที่ดินในพื้นที่สีแดงอาจแพงเกินกว่าจะทำบ้านพักอาศัยเพื่อความคุ้มค่า")
        else:
            risks.append("✅ พื้นที่ศักยภาพสูง: เหมาะแก่การปล่อยเช่าหรือทำธุรกิจ")
    
    elif zone == "Purple":
        if property_type in ["คอนโด", "อพาร์ทเม้นท์"]:
            risks.append("🚫 ข้อห้ามทางกฎหมาย: พื้นที่สีม่วง (อุตสาหกรรม) มักไม่อนุญาตให้สร้างที่อยู่อาศัยหนาแน่นสูง")
        else:
            risks.append("✅ พื้นที่ศักยภาพ: เหมาะสำหรับโกดัง คลังสินค้า หรือโรงงานขนาดเล็ก")
            
    # กฎข้อที่ 3: เช็คความเสี่ยงเสริมตามพื้นที่ (เช่น น้ำท่วม)
    if "พุทธมณฑล" in str(location_text) or "สามพราน" in str(location_text):
        risks.append("💧 ความเสี่ยงด้านภูมิประเทศ: พื้นที่ลุ่มต่ำ อาจมีความเสี่ยงน้ำท่วมในช่วงฤดูฝน")

    return risks
     
    
def check_profitability_risk(gain_annual):
    # ประมาณการค่าใช้จ่ายการขาย 8.8%
    if gain_annual < 8.8:
        return f"📉 ความเสี่ยงด้านกำไร: กำไรต่อปี ({gain_annual}%) ต่ำกว่าค่าใช้จ่ายในการขาย (8.8%) หากขายในระยะสั้นอาจขาดทุนสุทธิ"
    return None

def check_yield_risk(yield_pct):
    if yield_pct < 4.0:
        return "⚠️ ความเสี่ยงสภาพคล่อง: ผลตอบแทนจากการเช่าน้อยกว่า 4% อาจไม่คุ้มค่าหากต้องกู้เงินมาลงทุน"
    return "✅ ผลตอบแทนการเช่าอยู่ในเกณฑ์ดี"

# ---------------------------------------------------------
# ตัวอย่างการนำไปเรียกใช้ (สามารถลบออกได้ตอนนำไปใช้งานจริง)
if __name__ == "__main__":
    # ทดสอบจำลองดึงข้อมูลจาก Row ที่ 1 ของ CSV ของคุณ (ร้านขาย ที่ ศาลายา)
    sample_location = "ศาลายา, พุทธมณฑล"
    sample_type = "ร้านขาย"
    #
    print(f"พื้นที่: {sample_location}")
    print(f"โซนสี: {get_location_zone(sample_location)}")
    print("ผลการวิเคราะห์ความเสี่ยง:")
    for warning in check_city_plan_risk(sample_location, sample_type):
        print(" -", warning)