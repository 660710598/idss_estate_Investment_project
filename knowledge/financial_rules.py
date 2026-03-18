def evaluate_investment_tag(rental_yield, capital_gain, rules_dict):
    """ประเมินป้ายกำกับ (Tag) ตามตรรกะ If-Else"""
    tags = []
    
    # ดึงค่า Threshold จาก JSON
    target_yield = rules_dict['financial_criteria']['target_rental_yield_pct']
    target_gain = rules_dict['financial_criteria']['target_capital_gain_pct']
    
    # ตรวจสอบว่ามีข้อมูลผลตอบแทนหรือไม่
    if not isinstance(rental_yield, (int, float)) or not isinstance(capital_gain, (int, float)):
        return ["ข้อมูลไม่เพียงพอ"]

    # แก้ปัญหาเป้าหมายขัดแย้งด้วย Multi-tagging
       
       #ผลตอบแทนจากการเช่า >= ผลตอบแทนเป้าหมาย และ กำไรจากทุน >= กำไรเป้าหมาย
    if rental_yield >= target_yield and capital_gain >= target_gain:
        tags.append("สุดยอดทำเลทอง")
    #ผลตอบแทนจากการเช่า >= ผลตอบแทนเป้าหมาย
    if rental_yield >= target_yield:
        tags.append("เน้นปล่อยเช่า (Passive Income)")
    #กำไรจากทุน >= กำไรเป้าหมายd
    if capital_gain >= target_gain:
        tags.append("เน้นเก็งกำไร (Capital Gain)")
        
    return tags if tags else ["ผลตอบแทนต่ำกว่าเกณฑ์/รอดูสถานการณ์"]