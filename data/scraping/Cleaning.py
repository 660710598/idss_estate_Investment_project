import pandas as pd
import re
import numpy as np
import sqlite3

print("กำลังโหลดข้อมูลและเริ่มการทำความสะอาด (Data Cleaning)...")
df = pd.read_csv('data/scraping/NakhonPathom_Properties.csv')

# ฟังก์ชันตัวช่วยสำหรับดึงข้อมูลออกจากข้อความ
def extract_price(text):
    match = re.search(r'฿\s*([\d,]+)', str(text))
    if match:
        price_str = match.group(1).replace(',', '')
        return float(price_str)
    return np.nan

def extract_type(text):
    types = ['คอนโด', 'บ้านแฝด', 'บ้านเดี่ยว', 'ทาวน์โฮม', 'ทาวน์เฮ้าส์', 'ที่ดิน', 'อพาร์ทเม้นท์', 'อาคารพาณิชย์']
    for t in types:
        if t in str(text):
            return t
    return 'อื่นๆ'

def extract_location(text):
    text_str = str(text)
    
    # 1. ลองหาจาก ตำบล... อำเภอ... หรือ ต.... อ.... ก่อน
    exact_match = re.search(r'(?:ตำบล|ต\.)\s*([ก-๙a-zA-Z]+)\s*(?:อำเภอ|อ\.)\s*([ก-๙a-zA-Z]+)', text_str)
    
    if exact_match:
        loc = f"{exact_match.group(1).strip()}, {exact_match.group(2).strip()}"
    else:
        match = re.search(r'([ก-๙a-zA-Z\s]+),\s*([ก-๙a-zA-Z\s]+),\s*นครปฐม', text_str)
        if match:
            loc = f"{match.group(1).strip()}, {match.group(2).strip()}"
        else:
            match2 = re.search(r'([ก-๙a-zA-Z\s]+),\s*นครปฐม', text_str)
            if match2:
                loc = match2.group(1).strip()
            else:
                loc = 'นครปฐม (ไม่ระบุอำเภอ)'
            
    # 3. ตัดคำโฆษณาต่างๆ ออก เพื่อให้เหลือแค่ทำเลจริงๆ
    words_to_remove = ['ขาย', 'ให้เช่า', 'ด่วน', 'คอนโด', 'บ้านแฝด', 'บ้านเดี่ยว', 'ทาวน์โฮม', 'ทาวน์เฮ้าส์', 'ที่ดิน', 'อพาร์ทเม้นท์', 'อาคารพาณิชย์', 'หอพัก', 'ร้านของ', 'คลังสินค้า']
    
    for word in words_to_remove:
        loc = loc.replace(word, '')
        
    return loc.strip()

def extract_area(text):
    match = re.search(r'([\d,.]+)\s*(ตรม\.|ตร\.ว\.|ไร่)', str(text))
    if match:
        return match.group(0)
    return 'ไม่ระบุ'

# นำฟังก์ชันไปประยุกต์ใช้กับคอลัมน์ 
df['Price_THB'] = df['ชื่อประกาศ'].apply(extract_price)      
df['Area'] = df['ชื่อประกาศ'].apply(extract_area)
df['Property_Type'] = df['ชื่อประกาศ'].apply(extract_type) 
df['Location'] = df['ชื่อประกาศ'].apply(extract_location)


np.random.seed(8) 
def generate_idss_features_real_data(row):
    price = row['Price_THB']
    prop_type = str(row['Property_Type'])
    loc = str(row['Location'])

    if pd.isna(price) or price == 0:
        return np.nan, np.nan, np.nan

    # --- กำหนด Yield และ Capital Gain ตามข้อมูลอ้างอิงตลาดจริง ---
    if prop_type == 'คอนโด':
        # อ้างอิง: คอนโดนครปฐม Yield เฉลี่ย 3 - 4% และ CG เฉลี่ย 3.4 - 5%
        base_yield = np.random.uniform(0.030, 0.040)
        base_cg = np.random.uniform(3.4, 5.0) 
        
        # ล็อก Yield ให้สูงขึ้นอีกนิด หากอยู่ในทำเลนักศึกษา 
        if any(zone in loc for zone in ['ศาลายา', 'กำแพงแสน', 'เมืองนครปฐม']):
            base_yield = np.random.uniform(0.040, 0.060)

    elif prop_type in ['บ้านเดี่ยว', 'บ้านแฝด', 'ทาวน์เฮ้าส์', 'ทาวน์โฮม']:
        base_yield = np.random.uniform(0.035, 0.045)
        base_cg = np.random.uniform(5.0, 7.0)

    elif prop_type == 'ที่ดิน':
        base_yield = np.random.uniform(0.010, 0.020)
        base_cg = np.random.uniform(10.0, 15.0)
        
    elif prop_type == 'อพาร์ทเม้นท์' or 'หอพัก' in str(row['ชื่อประกาศ']):
        base_yield = np.random.uniform(0.060, 0.080)
        base_cg = np.random.uniform(2.0, 3.5)
        
    else:
        base_yield = np.random.uniform(0.040, 0.050)
        base_cg = np.random.uniform(3.0, 5.0)

    # สร้างค่าเช่ารายเดือนที่ดูสมจริง (ปัดเศษหลักร้อย)
    annual_rent = price * base_yield
    est_rent_month = round(annual_rent / 12, -2) 

    # คำนวณ Yield (%) กลับจากค่าเช่ารายเดือนที่ปัดเศษแล้ว 
    final_yield = ((est_rent_month * 12) / price) * 100

    return est_rent_month, round(final_yield, 2), round(base_cg, 2)

df[['Estimated_Rent_per_Month', 'Rental_Yield_Pct', 'Capital_Gain_Pct_Per_Year']] = df.apply(
    lambda row: pd.Series(generate_idss_features_real_data(row)), axis=1
)

df['Title_Clean'] = df['ชื่อประกาศ'].apply(lambda x: x.split('\n')[-1][:60] + "..." if isinstance(x, str) else x)

# จัดเรียงคอลัมน์ให้พร้อมสำหรับ Database
final_cols = ['Title_Clean', 'Property_Type', 'Location', 'Price_THB', 'Area', 'Estimated_Rent_per_Month', 'Rental_Yield_Pct', 'Capital_Gain_Pct_Per_Year', 'ลิงก์']
df_clean = df[final_cols].copy()

# ลบการขึ้นบรรทัดใหม่ทั้งหมดเพื่อให้ข้อมูลอยู่บรรทัดเดียว
for col in df_clean.select_dtypes(include=['object']).columns:
    df_clean[col] = df_clean[col].astype(str).str.replace(r'\n', ' ', regex=True).str.replace(r'\r', '', regex=True)

conn = sqlite3.connect('data/scraping/NakhonPathom_IDSS.db')
df.to_sql('properties', conn, if_exists='replace', index=False)
conn.close()

# บันทึกไฟล์ CSV 
output_filename = 'data/scraping/NakhonPathom_Properties_Cleaned.csv'
df_clean.to_csv(output_filename, index=False, encoding='utf-8-sig')
print(f"✅ ทำความสะอาดข้อมูลเสร็จสิ้น!")