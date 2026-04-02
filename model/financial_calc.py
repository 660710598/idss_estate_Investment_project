# models/financial_calc.py
def calculate_monthly_payment(principal, annual_interest_rate, years):
    """
    ฟังก์ชันคำนวณยอดผ่อนชำระต่อเดือน (What-If Analysis)
    ใช้สูตร M = P [ r(1 + r)^n ] / [ (1 + r)^n - 1 ]

    """
    if principal <= 0 or years <= 0:
        return 0
    if annual_interest_rate == 0:
        return principal / (years * 12)
        
    monthly_rate = (annual_interest_rate / 100) / 12
    num_payments = years * 12
    
    # คำนวณตามสูตรคณิตศาสตร์การเงิน
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    return round(payment, 2)


def get_affordability_flag(monthly_pay, monthly_income):
    # ฟังก์ชันประเมินภาระผ่อนเทียบกับรายได้ (Affordability Flag)
    if monthly_income <= 0:
        return "❓ ไม่ทราบรายได้"
    ratio = (monthly_pay / monthly_income) * 100
    if ratio < 30:
        return f"✅ ภาระผ่อนเหมาะสม ({ratio:.0f}% ของรายได้)"
    elif ratio < 40:
        return f"🟡 ภาระผ่อนปานกลาง ({ratio:.0f}% ของรายได้)"
    else:
        return f"⚠️ ภาระผ่อนสูง ({ratio:.0f}% ของรายได้)"
    

def calculate_investment_score(rental_yield, capital_gain, price, property_type, rules_dict):
    """
    ฟังก์ชันให้คะแนนความน่าลงทุน (เต็ม 10 คะแนน)
    ดึงเกณฑ์การให้คะแนนและหักคะแนนมาจาก expert_rules.json (Knowledge Base)
    """
    score = 5.0 # คะแนนเริ่มต้นที่ 5
    
    # ดึงกฎต่างๆ ออกมาจาก rules_dict
    criteria = rules_dict.get('investment_criteria', {})
    risk_weights = rules_dict.get('risk_scoring_weights', {})
    prop_suitability = rules_dict.get('property_type_suitability', {})
    
    # --- 1. การประเมินผลตอบแทน (Yield & Capital Gain) ---
    good_yield = criteria.get('good_rental_yield_pct', 7.0)
    min_yield = criteria.get('min_rental_yield_pct', 5.0)
    
    if rental_yield >= good_yield:
        score += 3.0
    elif rental_yield >= min_yield:
        score += 1.5
    else:
        score += risk_weights.get('low_yield_penalty', -2) # ดึงค่าหักคะแนน Yield ต่ำจาก JSON (-2)
        
    good_gain = criteria.get('good_capital_gain_pct', 5.0)
    min_gain = criteria.get('min_capital_gain_pct', 3.0)
    
    if capital_gain >= good_gain:
        score += 2.0
    elif capital_gain >= min_gain:
        score += 1.0
        
    # --- 2. การหักคะแนนความเสี่ยงด้านราคา (Liquidity Risk) ---
    if price > 10000000:
        score += risk_weights.get('high_price_penalty', -1) # ดึงค่าหักคะแนนราคาแพงจาก JSON (-1)
        
    # --- 3. ประเมินความเสี่ยงตามประเภทอสังหาฯ (Property Suitability) ---
    # จับคู่ชื่อภาษาไทยจาก CSV กับ Key ภาษาอังกฤษใน JSON
    prop_key = None
    if 'คอนโด' in property_type:
        prop_key = 'condo'
    elif 'ที่ดิน' in property_type:
        prop_key = 'land'
    elif property_type in ['บ้านเดี่ยว', 'ทาวน์โฮม', 'บ้านแฝด', 'บ้าน']:
        prop_key = 'house'
        
    if prop_key and prop_key in prop_suitability:
        risk_level = prop_suitability[prop_key].get('risk_level', 'medium')
        if risk_level == 'low':
            score += 1.0  # ความเสี่ยงต่ำ (เช่น บ้าน) ให้โบนัสคะแนน
        elif risk_level == 'high':
            score -= 1.0  # ความเสี่ยงสูง (เช่น ที่ดินเปล่า) หักคะแนน
            
    # ควบคุมคะแนนให้อยู่ในกรอบ 0.0 - 10.0
    return max(0.0, min(10.0, score))
