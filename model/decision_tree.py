
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

def calculate_investment_score(rental_yield, capital_gain, price):
    """
    ฟังก์ชันให้คะแนนความน่าลงทุน (เต็ม 10 คะแนน)
    ช่วยแก้ปัญหา Conflicting Objectives: อยากได้ผลตอบแทนสูง แต่ราคาต้องไม่แพงเว่อร์
    
    """
    score = 5.0 # คะแนนเริ่มต้น
    
    # 1. ดูผลตอบแทนจากการปล่อยเช่า (ยิ่งสูงยิ่งดี)
    if rental_yield >= 7.0:
        score += 3.0
    elif rental_yield >= 5.0:
        score += 1.5
        
    # 2. ดูการเติบโตของราคา (ยิ่งสูงยิ่งดี)
    if capital_gain >= 5.0:
        score += 2.0
    elif capital_gain >= 3.0:
        score += 1.0
        
    # 3. หักคะแนนถ้าราคาสูงเกินไป (สมมติว่าเกิน 10 ล้านถือว่าความเสี่ยงสภาพคล่องสูง)
    if price > 10000000:
        score -= 1.0
        
    # ควบคุมให้อยู่ในกรอบ 0 - 10
    return max(0.0, min(10.0, score))