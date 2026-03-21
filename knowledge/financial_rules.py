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

def calculate_net_gain(gain_per_year, holding_years):
    # 1. คำนวณกำไรดิบ
    gross_gain = gain_per_year * holding_years
    
    # 2. หักภาษีธุรกิจเฉพาะ (3.3%) ถ้าถือน้อยกว่า 5 ปี 
    # ถ้าถือเกิน 5 ปี เสียแค่อากรแสตมป์ (0.5%)
    tax = 3.3 if holding_years < 5 else 0.5
    
    # 3. กำไรสุทธิ (ลบค่าโอนกลางๆ อีก 1%)
    net_profit = gross_gain - tax - 1.0
    return net_profit

def get_sale_advice(net_profit):
    if net_profit > 10:
        return "💰 น่าขาย: กำไรคุ้มค่าเหนื่อย"
    elif net_profit > 0:
        return "👌 พอได้กำไร: แต่ไม่เยอะมาก"
    else:
        return "❌ อย่าเพิ่งขาย: หักภาษีแล้วอาจขาดทุนหรือเท่าทุน"
    
def estimate_mortgage(price, down_payment_pct=0):
    # 1. คำนวณยอดจัดกู้ (ราคาลบเงินดาวน์)
    loan_amount = price * (1 - (down_payment_pct / 100))
    
    # 2. ใช้สูตรลัด 1,000,000 ละ 7,000 บาท
    monthly_installment = (loan_amount / 1_000_000) * 7000
    
    return monthly_installment
def check_profitability_risk(gain_annual):
    # ประมาณการค่าใช้จ่ายการขาย 8.8%
    if gain_annual < 8.8:
        return f"📉 ความเสี่ยงด้านกำไร: กำไรต่อปี ({gain_annual}%) ต่ำกว่าค่าใช้จ่ายในการขาย (8.8%) หากขายในระยะสั้นอาจขาดทุนสุทธิ"
    return None

def check_yield_risk(yield_pct):
    if yield_pct < 4.0:
        return "⚠️ ความเสี่ยงสภาพคล่อง: ผลตอบแทนจากการเช่าน้อยกว่า 4% อาจไม่คุ้มค่าหากต้องกู้เงินมาลงทุน"
    return "✅ ผลตอบแทนการเช่าอยู่ในเกณฑ์ดี"