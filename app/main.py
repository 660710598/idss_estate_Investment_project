# app/main.py
import json
import sqlite3
import sys
import os
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.decision_tree import filter_and_rank_properties
from model.financial_calc import calculate_monthly_payment, get_affordability_flag

st.set_page_config(page_title="IDSS Real Estate Nakhon Pathom", layout="wide", page_icon="🏠")

# โหลดข้อมูลและ Knowledge Base
@st.cache_data
def load_data():
    conn = sqlite3.connect('data/scraping/NakhonPathom_IDSS.db')
    df = pd.read_sql_query("SELECT * FROM properties", conn)
    conn.close()
    return df

@st.cache_data
def load_rules():
    # FIX: โหลด expert_rules.json เพื่อส่งเข้า filter_and_rank_properties()
    with open('knowledge/expert_rules.json', 'r', encoding='utf-8') as f:
        return json.load(f)

df = load_data()
rules_dict = load_rules()

# 1. Sidebar: Intelligence Phase
st.sidebar.header("🎯 กำหนดเงื่อนไขการลงทุน")
st.sidebar.markdown("*(Intelligence Phase)*")

user_budget = st.sidebar.number_input(
    "งบประมาณสูงสุด (บาท)",
    min_value=500000, max_value=50000000, value=5000000, step=500000
)

property_types = df['Property_Type'].dropna().unique().tolist()
user_property_type = st.sidebar.selectbox("ประเภทอสังหาริมทรัพย์", property_types)

locations = ["ศาลายา", "พุทธมณฑล", "เมืองนครปฐม","สนามจันทร์", "ห้วยจรเข้", "พระปฐมเจดีย์", "สามพราน", "กำแพงแสน", "นครชัยศรี", "ดอนตูม", "อ้อมใหญ่", "ไร่ขิง", "กระทุ่มล้ม", "ทุ่งลูกนก", "บางเลน", "ทุ่งกระพังโหม", "คลองโยง"]
user_location = st.sidebar.selectbox("ทำเลที่สนใจ", locations)

st.sidebar.divider()
st.sidebar.subheader("🏦 เงื่อนไขสินเชื่อ (What-If Parameters)")
down_payment_pct = st.sidebar.slider("เงินดาวน์ (%)", 0, 50, 10)
interest_rate    = st.sidebar.slider("ดอกเบี้ยเงินกู้ (% ต่อปี)", 1.0, 10.0, 3.5, step=0.1)
loan_years       = st.sidebar.slider("ระยะเวลาผ่อน (ปี)", 5, 40, 30)

st.sidebar.divider()
st.sidebar.subheader("💼 ข้อมูลรายได้ (Affordability Check)")
monthly_income = st.sidebar.number_input(
    "รายได้ต่อเดือน (บาท)",
    min_value=10000, max_value=500000, value=50000, step=5000
)

# 2. Main Area
st.title("🏠 ระบบสนับสนุนการตัดสินใจลงทุนอสังหาฯ จ.นครปฐม (IDSS)")
st.markdown("ระบบประเมินความเสี่ยง วิเคราะห์ผังเมือง และจัดอันดับความคุ้มค่า เพื่อช่วยสนับสนุนการตัดสินใจของคุณ")

if st.sidebar.button("🔍 วิเคราะห์หาตัวเลือกที่ดีที่สุด", type="primary"):

    with st.spinner('กำลังวิเคราะห์ข้อมูล ผังเมือง และประเมินความเสี่ยง...'):
        # FIX: เพิ่ม rules_dict เป็น argument ที่ 5
        result_df = filter_and_rank_properties(
            df, user_budget, user_location, user_property_type, rules_dict
        )

    if result_df.empty:
        st.warning(
            f"😔 ไม่พบ {user_property_type} ในย่าน {user_location} "
            f"ที่ราคาต่ำกว่า {user_budget:,.0f} บาท ลองปรับเงื่อนไขใหม่นะครับ"
        )
    else:
        safe_count  = len(result_df[result_df['Risk_Level'] == '✅ ผ่านเกณฑ์'])
        risky_count = len(result_df[result_df['Risk_Level'] == '🚫 ความเสี่ยงสูง'])
        st.success(f"🎉 พบทั้งหมด {len(result_df)} แห่ง — ✅ ผ่านเกณฑ์ {safe_count} แห่ง / 🚫 ความเสี่ยงสูง {risky_count} แห่ง")

        top_3 = result_df.head(3)
        st.subheader("🏆 Top 3 ทางเลือกที่คุ้มค่าที่สุด (Best Alternatives)")
        cols = st.columns(3)

        for i, (index, row) in enumerate(top_3.iterrows()):
            with cols[i]:
                risk_level = row.get('Risk_Level', '')
                # ย้าย if/else เข้ามาอยู่ใน with cols[i]: ด้วย
                if risk_level == '🚫 ความเสี่ยงสูง':
                    st.error(f"**อันดับ {i+1}** (คะแนน: {row['Investment_Score']:.1f}/10) — 🚫 ความเสี่ยงสูง")
                else:
                    st.info(f"**อันดับ {i+1}** (คะแนน: {row['Investment_Score']:.1f}/10)")

                # แสดงรายละเอียดทุก card ไม่ว่าจะ safe หรือ risky
                st.markdown(f"**{str(row['Title_Clean'])[:50]}...**")
                st.write(f"📍 **ทำเล:** {row['Location']}")
                st.write(f"📐 **พื้นที่:** {row['Area']}")
                st.write(f"💰 **ราคาขาย:** {row['Price_THB']:,.0f} บาท")

                tags = row.get('Investment_Tags', [])
                if isinstance(tags, list) and tags:
                    st.write(f"🏷️ **กลยุทธ์:** {', '.join(tags)}")

                loan_amount = row['Price_THB'] * (1 - down_payment_pct / 100)
                monthly_pay = calculate_monthly_payment(loan_amount, interest_rate, loan_years)
                st.metric(label="📉 ยอดผ่อนโดยประมาณ", value=f"฿{monthly_pay:,.0f} / เดือน")

                # Affordability Flag
                flag = get_affordability_flag(monthly_pay, monthly_income)
                st.markdown(f"**{flag}**")

                net_profit = row.get('Net_Profit_5Y', None)
                sale_advice = row.get('Sale_Advice', '')
                if net_profit is not None:
                    st.write(f"📈 **กำไรสุทธิ 5 ปี (หักภาษี):** {net_profit:.1f}%")
                if sale_advice:
                    st.write(f"💡 **คำแนะนำ:** {sale_advice}")

                with st.expander("⚠️ ดูรายงานความเสี่ยง (Risk Warnings)"):
                    warnings = str(row['Risk_Warnings']).split(" | ")
                    for w in warnings:
                        if w and w != "nan":
                            st.write(f"- {w}")

                if pd.notna(row.get('ลิงก์')):
                    st.markdown(f"[🔗 ไปยังประกาศหน้าเว็บ]({row['ลิงก์']})")

        st.divider()

        # 3. ตารางผลลัพธ์ทั้งหมด
        st.subheader("📊 ข้อมูลทางเลือกทั้งหมดที่ผ่านเกณฑ์")

        display_cols = [
            'Title_Clean', 'Location', 'Price_THB', 'Area',
            'Rental_Yield_Pct', 'Capital_Gain_Pct_Per_Year',
            'Investment_Score', 'Risk_Level',
            'Investment_Tags','Net_Profit_5Y', 'Sale_Advice', 'Risk_Warnings'
        ]
        display_cols = [c for c in display_cols if c in result_df.columns]
        display_df = result_df[display_cols].copy()

        display_df['Investment_Tags'] = display_df['Investment_Tags'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else str(x)
        )

        table_cols = [c for c in display_cols if c != 'Risk_Warnings']
        table_df = display_df[table_cols].copy()

        st.dataframe(
            table_df.style.background_gradient(
                subset=['Investment_Score'], cmap='RdYlGn', vmin=0, vmax=10
            ).format({
                'Price_THB': '{:,.0f}',
                'Rental_Yield_Pct': '{:.2f}%',
                'Capital_Gain_Pct_Per_Year': '{:.2f}%',
                'Investment_Score': '{:.1f}',
                'Net_Profit_5Y': '{:.1f}%',
            }),
            use_container_width=True
        )

        st.markdown("**⚠️ รายละเอียดความเสี่ยงทั้งหมด**")
        risk_df = display_df[['Title_Clean', 'Location', 'Risk_Warnings']].copy()
        risk_df['Risk_Warnings'] = risk_df['Risk_Warnings'].str.replace(' | ', '\n', regex=False)
        st.dataframe(risk_df, use_container_width=True, height=300)

else:
    st.info("👈 กรุณาปรับเงื่อนไขด้านซ้ายมือ แล้วกดปุ่ม 'วิเคราะห์หาตัวเลือกที่ดีที่สุด'")