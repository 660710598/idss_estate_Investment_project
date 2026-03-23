# models/decision_tree.py
import pandas as pd
from model.financial_calc import calculate_investment_score
from knowledge.city_plan_rules import check_city_plan_risk
from knowledge.financial_rules import (
    evaluate_investment_tag,
    check_investment_risk,
    calculate_net_gain,
    get_sale_advice,
)

# ฟังก์ชันหลักในการกรองและจัดอันดับอสังหาริมทรัพย์ตามเงื่อนไขของผู้ใช้
def filter_and_rank_properties(df, user_budget, user_location, user_property_type, rules_dict):
    filtered_df = df[
        (df['Price_THB'] <= user_budget) &
        (df['Location'].str.contains(user_location, na=False)) &
        (df['Property_Type'] == user_property_type)
    ].copy()

    if filtered_df.empty:
        return filtered_df

    # ฟังก์ชันช่วยดึงความเสี่ยงทั้งหมดจากทั้งผังเมืองและการเงิน
    def get_all_risks(row):
        risks = []
        # เช็คความเสี่ยงตามผังเมือง
        risks.extend(check_city_plan_risk(row['Location'], row['Property_Type']))

        # เช็คความเสี่ยงทางการเงินถ้ามีข้อมูลเพียงพอ
        if pd.notna(row['Rental_Yield_Pct']) and pd.notna(row['Capital_Gain_Pct_Per_Year']):
            risks.extend(check_investment_risk(row['Rental_Yield_Pct'], row['Capital_Gain_Pct_Per_Year']))
        return " | ".join(risks)

    # Risk Assessment
    filtered_df['Risk_Warnings'] = filtered_df.apply(get_all_risks, axis=1)
    filtered_df['Risk_Level'] = filtered_df['Risk_Warnings'].apply(
        lambda x: '🚫 ความเสี่ยงสูง' if 'ความเสี่ยงสูง:' in str(x) else '✅ ผ่านเกณฑ์'
    )

    # Investment Tags
    filtered_df['Investment_Tags'] = filtered_df.apply(
        lambda row: evaluate_investment_tag(
            row['Rental_Yield_Pct'],
            row['Capital_Gain_Pct_Per_Year'],
            rules_dict
        ), axis=1
    )

    # Net Gain & Sale Advice
    filtered_df['Net_Profit_5Y'] = filtered_df['Capital_Gain_Pct_Per_Year'].apply(
        lambda x: calculate_net_gain(x, holding_years=5)
    )
    filtered_df['Sale_Advice'] = filtered_df['Net_Profit_5Y'].apply(get_sale_advice)

    # Investment Score
    filtered_df['Investment_Score'] = filtered_df.apply(
        lambda row: calculate_investment_score(
            row['Rental_Yield_Pct'],
            row['Capital_Gain_Pct_Per_Year'],
            row['Price_THB']
        ), axis=1
    )

    # 5. Sort — ผ่านเกณฑ์ขึ้นก่อน ความเสี่ยงสูงอยู่ท้าย (return ที่เดียว ท้ายสุด)
    safe_df  = filtered_df[filtered_df['Risk_Level'] == '✅ ผ่านเกณฑ์'].sort_values('Investment_Score', ascending=False)
    risky_df = filtered_df[filtered_df['Risk_Level'] == '🚫 ความเสี่ยงสูง'].sort_values('Investment_Score', ascending=False)

    return pd.concat([safe_df, risky_df], ignore_index=True)