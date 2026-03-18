# app/main.py
import streamlit as st
import pandas as pd
import sys
import os

# เพิ่มพาธเพื่อให้ Streamlit มองเห็นโฟลเดอร์ models และ knowledge_base
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.decision_tree import filter_and_rank_properties
from model.financial_calc import calculate_monthly_payment

# ตั้งค่าหน้าเพจ
st.set_page_config(page_title="IDSS Real Estate Nakhon Pathom", layout="wide", page_icon="🏠")

# โหลดข้อมูล (ใช้ st.cache_data เพื่อไม่ให้โหลดใหม่ทุกครั้งที่ขยับเมาส์)
@st.cache_data
def load_data():
    # ปรับพาธให้ชี้ไปที่ไฟล์ CSV ของคุณ
    return pd.read_csv('data/scraping/NakhonPathom_Properties_Cleaned.csv')

df = load_data()

# ==========================================
# 1. Sidebar: ส่วนรับข้อมูล (Intelligence Phase)
# ==========================================
st.sidebar.header("🎯 กำหนดเงื่อนไขการลงทุน")
st.sidebar.markdown("*(Intelligence Phase)*")

# ข้อจำกัดด้านงบประมาณ
user_budget = st.sidebar.number_input("งบประมาณสูงสุด (บาท)", min_value=500000, max_value=50000000, value=5000000, step=500000)

# ข้อจำกัดด้านความต้องการ (ดึงค่า Unique จาก CSV มาเป็นตัวเลือก)
property_types = df['Property_Type'].dropna().unique().tolist()
user_property_type = st.sidebar.selectbox("ประเภทอสังหาริมทรัพย์", property_types)

# จำลองรายชื่อทำเลหลักๆ (คุณสามารถดึงจาก unique() ของคอลัมน์ Location ได้เช่นกัน)
locations = ["ศาลายา", "พุทธมณฑล", "เมืองนครปฐม", "สามพราน", "กำแพงแสน", "นครชัยศรี"]
user_location = st.sidebar.selectbox("ทำเลที่สนใจ (ระบุคำค้นหา)", locations)

st.sidebar.divider()
st.sidebar.subheader("🏦 เงื่อนไขสินเชื่อ (What-If Parameters)")
down_payment_pct = st.sidebar.slider("เงินดาวน์ (%)", 0, 50, 10)
interest_rate = st.sidebar.slider("ดอกเบี้ยเงินกู้ (% ต่อปี)", 1.0, 10.0, 3.5, step=0.1)
loan_years = st.sidebar.slider("ระยะเวลาผ่อน (ปี)", 5, 40, 30)

# ==========================================
# 2. Main Area: ส่วนแสดงผล (Design & Choice Phase)
# ==========================================
st.title("🏠 ระบบสนับสนุนการตัดสินใจลงทุนอสังหาฯ จ.นครปฐม (IDSS)")
st.markdown("ระบบประเมินความเสี่ยง วิเคราะห์ผังเมือง และจัดอันดับความคุ้มค่า เพื่อช่วยสนับสนุนการตัดสินใจของคุณ")

# ปุ่มกดเพื่อเริ่มประมวลผล
if st.sidebar.button("🔍 วิเคราะห์หาตัวเลือกที่ดีที่สุด", type="primary"):
    
    # เรียกใช้ Model (Decision Logic) จากไฟล์ decision_tree.py
    with st.spinner('กำลังวิเคราะห์ข้อมูล ผังเมือง และประเมินความเสี่ยง...'):
        result_df = filter_and_rank_properties(df, user_budget, user_location, user_property_type)
    
    if result_df.empty:
        st.warning(f"😔 ไม่พบ {user_property_type} ในย่าน {user_location} ที่ราคาต่ำกว่า {user_budget:,.0f} บาท ลองปรับเงื่อนไขใหม่นะครับ")
    else:
        st.success(f"🎉 พบตัวเลือกที่ผ่านเกณฑ์จำนวน {len(result_df)} แห่ง (คัดกรองความเสี่ยงผังเมืองแล้ว)")
        
        # ดึง Top 3 มาแสดงผล
        top_3 = result_df.head(3)
        
        st.subheader("🏆 Top 3 ทางเลือกที่คุ้มค่าที่สุด (Best Alternatives)")
        
        # สร้าง 3 คอลัมน์เพื่อแสดงเป็น Card สวยๆ
        cols = st.columns(3)
        
        for i, (index, row) in enumerate(top_3.iterrows()):
            with cols[i]:
                st.info(f"**อันดับ {i+1}** (คะแนน: {row['Investment_Score']:.1f}/10)")
                st.markdown(f"**{row['Title_Clean'][:50]}...**")
                st.write(f"📍 **ทำเล:** {row['Location']}")
                st.write(f"📐 **พื้นที่:** {row['Area']}")
                st.write(f"💰 **ราคาขาย:** {row['Price_THB']:,.0f} บาท")
                
                # คำนวณ What-If ยอดผ่อนต่อเดือน
                loan_amount = row['Price_THB'] * (1 - (down_payment_pct/100))
                monthly_pay = calculate_monthly_payment(loan_amount, interest_rate, loan_years)
                st.metric(label="📉 ยอดผ่อนโดยประมาณ", value=f"฿{monthly_pay:,.0f} / เดือน")
                
                # แสดงคำเตือนความเสี่ยง (จาก Knowledgebase)
                with st.expander("⚠️ ดูรายงานความเสี่ยง (Risk Warnings)"):
                    warnings = str(row['Risk_Warnings']).split(" | ")
                    for w in warnings:
                        if w and w != "nan":
                            st.write(f"- {w}")
                
                # ปุ่มลิงก์ไปดูของจริง
                if pd.notna(row['ลิงก์']):
                    st.markdown(f"[🔗 ไปยังประกาศหน้าเว็บ]({row['ลิงก์']})")

        st.divider()
        
        # ==========================================
        # 3. Data Visualization & What-If Analysis
        # ==========================================
        st.subheader("📊 ข้อมูลทางเลือกทั้งหมดที่ผ่านเกณฑ์")
        # โชว์ตารางแบบเลือกคอลัมน์สำคัญๆ มาโชว์
        display_df = result_df[['Title_Clean', 'Price_THB', 'Area', 'Rental_Yield_Pct', 'Capital_Gain_Pct_Per_Year', 'Investment_Score', 'Risk_Warnings']].copy()
        st.dataframe(display_df.style.highlight_max(axis=0, subset=['Investment_Score'], color='#90EE90'))
        
else:
    st.info("👈 กรุณาปรับเงื่อนไขด้านซ้ายมือ แล้วกดปุ่ม 'วิเคราะห์หาตัวเลือกที่ดีที่สุด'")