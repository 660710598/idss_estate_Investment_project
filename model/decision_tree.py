# models/decision_tree.py
import pandas as pd
from model.financial_calc import calculate_investment_score
from knowledge.city_plan_rules import check_city_plan_risk,check_profitability_risk, check_yield_risk

def filter_and_rank_properties(df, user_budget, user_location, user_property_type):
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
        # เช็คความเสี่ยงที่ 1: กฎหมายผังเมือง
        risks.extend(check_city_plan_risk(row['Location'], row['Property_Type']))
        
        # เช็คความเสี่ยงที่ 2: ผลตอบแทนค่าเช่า (Yield Risk)
        if pd.notna(row['Rental_Yield_Pct']):
            yield_warning = check_yield_risk(row['Rental_Yield_Pct'])
            if yield_warning:
                risks.append(yield_warning)
            
        # เช็คความเสี่ยงที่ 3: กำไรส่วนทุน (Profitability Risk)
        if pd.notna(row['Capital_Gain_Pct_Per_Year']):
            profit_warning = check_profitability_risk(row['Capital_Gain_Pct_Per_Year'])
            if profit_warning:
                risks.append(profit_warning)
            
        return " | ".join(risks)

    # Knowledgebase Application: นำฟังก์ชันรวมความเสี่ยงไปประยุกต์ใช้กับทุกแถวใน DataFrame
    filtered_df['Risk_Warnings'] = filtered_df.apply(get_all_risks, axis=1)
    
    # ตัดตัวเลือกที่มี "ความเสี่ยงสูง" ออกจากระบบ (Decision Rule)
    filtered_df = filtered_df[~filtered_df['Risk_Warnings'].str.contains("ความเสี่ยงสูง:")]
    
    # 3. Choice Phase: ให้คะแนนและจัดอันดับ (Scoring)
    filtered_df['Investment_Score'] = filtered_df.apply(
        lambda row: calculate_investment_score(
            row['Rental_Yield_Pct'], 
            row['Capital_Gain_Pct_Per_Year'], 
            row['Price_THB']
        ), 
        axis=1
    )
    
    # จัดอันดับจากคะแนนมากไปน้อย
    ranked_df = filtered_df.sort_values(by='Investment_Score', ascending=False)
    
    # ส่งคืนผลลัพธ์เพื่อนำไปแสดงบน UI
    return ranked_df

