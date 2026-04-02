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

def check_investment_risk(yield_pct, gain_annual, rules_dict):
    criteria = rules_dict.get('investment_criteria', {})
    risk_yield = criteria.get('risk_rental_yield_pct', 4.0)
    risk_gain = criteria.get('risk_capital_gain_pct', 8.8)

    risks = []
    if yield_pct < risk_yield:
        risks.append("⚠️ ความเสี่ยงสภาพคล่อง: Yield ต่ำกว่า 4%")
    
    # ใช้ 8.8% เป็นจุดตัดความเสี่ยง (Break-even point)
    if gain_annual < risk_gain:
        risks.append(f"📉 ความเสี่ยงกำไร: กำไร {gain_annual}% ยังไม่คลุมค่าใช้จ่ายแฝง (8.8%)")
    return risks

def calculate_net_gain(gain_per_year, holding_years):
    """คำนวณกำไรสุทธิหลังหักภาษีและค่าโอน"""
    gross_gain = gain_per_year * holding_years
    tax = 3.3 if holding_years < 5 else 0.5
    return gross_gain - tax - 1.0

def get_sale_advice(net_profit):
    if net_profit >= 20:
        return "💰 น่าซื้อขาย: กำไรสูง คุ้มค่าเหนื่อยและการลงทุน"
    elif net_profit >= 10:
        return "👌 พอได้กำไร: ชนะเงินเฟ้อ แต่เทียบฝากประจำอาจไม่คุ้มค่าเสียโอกาส"
    else:
        return "❌ อย่าเพิ่งขาย: กำไรต่ำเกินไป หักค่าใช้จ่ายแฝงแล้วอาจเข้าเนื้อ"


