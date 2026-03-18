# models/decision_tree.py
import pandas as pd
# ดึงฟังก์ชันมาจากไฟล์อื่นที่เราสร้างไว้
from models.financial_calc import calculate_investment_score
from knowledge_base.city_plan_rules import check_city_plan_risk

def filter_and_rank_properties(df, user_budget, user_location, user_property_type):
    """
    กระบวนการตัดสินใจ (Decision Logic)
    รับ DataFrame และเงื่อนไขผู้ใช้ แล้วคืนค่า Top ทางเลือกที่ดีที่สุด

    ขั้นตอน:
    1. Design Phase: คัดกรองเบื้องต้นตามงบและความต้องการ
    2. Knowledgebase Application: ประเมินความเสี่ยงตามกฎผู้เชี่ยวชาญ
    3. Choice Phase: ให้คะแนนและจัดอันดับทางเลือกที่เหลือ
    """
    # 1. Design Phase: คัดกรองเบื้องต้น (Budget & Preference)
    filtered_df = df[
        (df['Price_THB'] <= user_budget) & 
        (df['Location'].str.contains(user_location, na=False)) &
        (df['Property_Type'] == user_property_type)
    ].copy()
    
    # ถ้าไม่มีข้อมูลผ่านเกณฑ์เลย คืนค่าเป็น DataFrame ว่างๆ ก็จะตีกลับไป
    if filtered_df.empty:
        return filtered_df
        
    # 2. Knowledgebase Application: นำกฎผู้เชี่ยวชาญมาประเมินความเสี่ยง
    # สร้างคอลัมน์ใหม่เก็บข้อความแจ้งเตือนความเสี่ยง
    filtered_df['Risk_Warnings'] = filtered_df.apply(
        lambda row: ", ".join(check_city_plan_risk(row['Location'], row['Property_Type'])), 
        axis=1
    )
    
    # ตัดตัวเลือกที่มี "ความเสี่ยงสูง" ออกจากระบบ (Decision Rule)
    filtered_df = filtered_df[~filtered_df['Risk_Warnings'].str.contains("ความเสี่ยงสูง")]
    
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

# ---------------------------------------------------------
# ตัวอย่างการนำไปเรียกใช้ (ลบออกได้ตอนใช้งานจริง)
if __name__ == "__main__":
    # จำลองการโหลดข้อมูล
    try:
        df = pd.read_csv('../NakhonPathom_Properties_Cleaned.csv')
        # จำลองผู้ใช้: มีงบ 5 ล้าน, อยากได้ร้านขายของ, แถวศาลายา
        result = filter_and_rank_properties(df, user_budget=5000000, user_location="ศาลายา", user_property_type="ร้านขาย")
        print(f"เจอทางเลือกทั้งหมด: {len(result)} แห่ง")
        print(result[['Title_Clean', 'Price_THB', 'Investment_Score', 'Risk_Warnings']].head(3))
    except FileNotFoundError:
        print("กรุณารันจากตำแหน่งที่มองเห็นไฟล์ CSV")