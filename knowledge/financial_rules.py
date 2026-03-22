def evaluate_investment_tag(rental_yield, capital_gain, rules_dict):
    """ประเมินป้ายกำกับ (Tag) โดยใช้เกณฑ์จาก JSON"""
    tags = []
    
    # ดึงค่าเกณฑ์จาก JSON (ใช้ชื่อ Key ให้ตรงกับไฟล์ที่คุณส่งมา)
    criteria = rules_dict.get('investment_criteria', {})
    min_yield = criteria.get('min_rental_yield_pct', 5.0)
    min_gain = criteria.get('min_capital_gain_pct', 3.0)
    
    if not isinstance(rental_yield, (int, float)) or not isinstance(capital_gain, (int, float)):
        return ["ข้อมูลไม่เพียงพอ"]

    # 1. เช็คความคุ้มค่า (ยุบรวม logic ให้ใช้เกณฑ์จาก JSON ที่เดียว)
    if rental_yield >= min_yield and capital_gain >= min_gain:
        tags.append("🌟 สุดยอดทำเลทอง")
    elif rental_yield >= min_yield:
        tags.append("💰 เน้นปล่อยเช่า (Passive Income)")
    elif capital_gain >= min_gain:
        tags.append("📈 เน้นเก็งกำไร (Capital Gain)")
        
    return tags if tags else ["⚪ รอดูสถานการณ์"]

def check_investment_risk(yield_pct, gain_annual):
    risks = []
    if yield_pct < 4.0:
        risks.append("⚠️ ความเสี่ยงสภาพคล่อง: Yield ต่ำกว่า 4%")
    
    # ใช้ 8.8% เป็นจุดตัดความเสี่ยง (Break-even point)
    if gain_annual < 8.8:
        risks.append(f"📉 ความเสี่ยงกำไร: กำไร {gain_annual}% ยังไม่คลุมค่าใช้จ่ายแฝง (8.8%)")
    return risks

def calculate_net_gain(gain_per_year, holding_years):
    """คำนวณกำไรสุทธิหลังหักภาษีและค่าโอน"""
    gross_gain = gain_per_year * holding_years
    tax = 3.3 if holding_years < 5 else 0.5
    return gross_gain - tax - 1.0

def get_sale_advice(net_profit):
    
    if net_profit > 10:
        return "💰 น่าขาย: กำไรคุ้มค่าเหนื่อย"
    elif net_profit > 0:
        return "👌 พอได้กำไร: ดีกว่าถือไว้เฉยๆ"
    else:
        return "❌ อย่าเพิ่งขาย: หักภาษีและค่าใช้จ่ายแล้วอาจขาดทุน"

def estimate_mortgage(price, down_payment_pct=0):
    """คำนวณเงินผ่อนเบื้องต้น (1 ล้านละ 7,000)"""
    loan_amount = price * (1 - (down_payment_pct / 100))
    return (loan_amount / 1_000_000) * 7000