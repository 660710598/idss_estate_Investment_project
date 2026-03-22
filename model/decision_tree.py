# models/decision_tree.py
import pandas as pd
from model.financial_calc import calculate_investment_score
from knowledge.city_plan_rules import check_city_plan_risk
from knowledge.financial_rules import (
    evaluate_investment_tag, 
    check_investment_risk, 
    calculate_net_gain, 
    get_sale_advice, 
    estimate_mortgage
)

def filter_and_rank_properties(df, user_budget, user_location, user_property_type, rules_dict):
    filtered_df = df[
        (df['Price_THB'] <= user_budget) & 
        (df['Location'].str.contains(user_location, na=False)) &
        (df['Property_Type'] == user_property_type)
    ].copy()
    
    # ถ้าไม่มีข้อมูลผ่านเกณฑ์เลย คืนค่าเป็น DataFrame ว่างๆ ก็จะตีกลับไป
    if filtered_df.empty:
        return filtered_df
        
    def get_all_risks(row):
            risks = []
            # เช็คความเสี่ยงที่ 1: กฎหมายผังเมือง (เดิม)
            risks.extend(check_city_plan_risk(row['Location'], row['Property_Type']))
            
            # เช็คความเสี่ยงที่ 2: ความเสี่ยงทางการเงิน (ใหม่)
            # จะเตือนถ้า Yield < 4% หรือ Gain < 8.8% ตามที่คุณเขียนไว้ใน financial_rules
            fin_risks = check_investment_risk(row['Rental_Yield_Pct'], row['Capital_Gain_Pct_Per_Year'])
            risks.extend(fin_risks)
                
            return " | ".join(risks)

        
    filtered_df['Risk_Warnings'] = filtered_df.apply(get_all_risks, axis=1)

            # Knowledgebase Application: นำฟังก์ชันรวมความเสี่ยงไปประยุกต์ใช้กับทุกแถวใน DataFrame
    filtered_df = filtered_df[~filtered_df['Risk_Warnings'].str.contains("ความเสี่ยงสูง:")]
    # 3. Choice Phase: ให้คะแนนและจัดอันดับ (Scoring)
    filtered_df['Investment_Tags'] = filtered_df.apply(
        lambda row: evaluate_investment_tag(
            row['Rental_Yield_Pct'], 
            row['Capital_Gain_Pct_Per_Year'], 
            rules_dict
        ), axis=1
    )
    
   # 2. คำนวณกำไรสุทธิหลังหักภาษี (Net Gain) - สมมติถือครอง 5 ปี
    filtered_df['Net_Profit_5Y'] = filtered_df['Capital_Gain_Pct_Per_Year'].apply(
        lambda x: calculate_net_gain(x, holding_years=5)
    )

    # 3. ให้คำแนะนำเชิงกลยุทธ์ (Sale Advice)
    filtered_df['Sale_Advice'] = filtered_df['Net_Profit_5Y'].apply(get_sale_advice)

    # 4. ประมาณยอดผ่อนต่อเดือนเบื้องต้น
    filtered_df['Monthly_Payment_Est'] = filtered_df['Price_THB'].apply(
        lambda x: estimate_mortgage(x) * 7000
    )

    # --- ส่วนการให้คะแนนและจัดอันดับ (Scoring Phase) ---
    filtered_df['Investment_Score'] = filtered_df.apply(
        lambda row: calculate_investment_score(
            row['Rental_Yield_Pct'], 
            row['Capital_Gain_Pct_Per_Year'], 
            row['Price_THB']
        ), axis=1
    )
    
    return filtered_df.sort_values(by='Investment_Score', ascending=False)
    # ส่งคืนผลลัพธ์เพื่อนำไปแสดงบน UI
    return ranked_df
