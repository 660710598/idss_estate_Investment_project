import pandas as pd
import numpy as np
import sqlite3
import random

np.random.seed(8)
n_rows = 500
data = []

# สัดส่วนข้อมูลที่จะ Generate (Condo 250, House 150, Apartment 100)
for _ in range(250):
    # คอนโด: สุ่มว่าเป็น กทม. หรือ นครปฐม
    location = random.choices(['Bangkok_CBD', 'Bangkok_Suburb', 'NakhonPathom_Campus'], weights=[0.4, 0.4, 0.2])[0]
    if location == 'Bangkok_CBD':
        price = np.random.randint(5_000_000, 15_000_000)
        yield_pct = round(np.random.uniform(4.0, 5.0), 2)
        cap_gain = round(np.random.uniform(3.0, 6.0), 2)
    elif location == 'Bangkok_Suburb':
        price = np.random.randint(2_000_000, 5_000_000)
        yield_pct = round(np.random.uniform(5.0, 6.5), 2)
        cap_gain = round(np.random.uniform(2.5, 4.5), 2)
    else: # NakhonPathom_Campus
        price = np.random.randint(850_000, 1_800_000)
        yield_pct = round(np.random.uniform(5.5, 7.5), 2) # Yield สูงเพราะราคาถูกและปล่อยเช่านักศึกษาได้ราคาดี
        cap_gain = round(np.random.uniform(1.5, 3.0), 2)
    data.append(['Condo', location, price, yield_pct, cap_gain])

for _ in range(150):
    # บ้าน: เน้น กทม.รอบนอก และ นครปฐม
    location = random.choices(['Bangkok_Suburb', 'NakhonPathom_City'], weights=[0.6, 0.4])[0]
    if location == 'Bangkok_Suburb':
        price = np.random.randint(5_000_000, 20_000_000)
        yield_pct = round(np.random.uniform(3.0, 4.5), 2)
        cap_gain = round(np.random.uniform(4.0, 7.0), 2) # บ้านได้ Capital gain ที่ดินสูง
    else:
        price = np.random.randint(3_000_000, 7_000_000)
        yield_pct = round(np.random.uniform(3.0, 4.0), 2)
        cap_gain = round(np.random.uniform(2.0, 5.0), 2)
    data.append(['House', location, price, yield_pct, cap_gain])

for _ in range(100):
    # อพาร์ทเม้นท์ (ซื้อตึกลงทุน): กระแสเงินสดดี
    location = random.choices(['Bangkok_Suburb', 'NakhonPathom_Campus'], weights=[0.5, 0.5])[0]
    if location == 'Bangkok_Suburb':
        price = np.random.randint(20_000_000, 50_000_000)
        yield_pct = round(np.random.uniform(6.0, 8.0), 2)
    else: # นครปฐมใกล้มอ
        price = np.random.randint(15_000_000, 35_000_000)
        yield_pct = round(np.random.uniform(7.0, 9.0), 2)
    cap_gain = round(np.random.uniform(1.0, 2.5), 2) # Capital gain ไม่สูงเทียบคอนโด/บ้าน
    data.append(['Apartment_Bldg', location, price, yield_pct, cap_gain])

# แปลงเป็น DataFrame และสลับแถว (Shuffle)
columns = ['Property_Type', 'Location_Zone', 'Price_THB', 'Rental_Yield_Pct', 'Capital_Gain_Pct']
df = pd.DataFrame(data, columns=columns)
df = df.sample(frac=1).reset_index(drop=True)
df.insert(0, 'Property_ID', range(1, len(df) + 1))

# บันทึกลง SQLite
conn = sqlite3.connect('data/generate/real_estate_idss.db')
df.to_sql('properties', conn, if_exists='replace', index=False)
conn.close()

df.to_csv('data/generate/real_estate_data.csv', index=False)

print("สร้างข้อมูลเสร็จสมบูรณ์และบันทึกลงฐานข้อมูลเรียบร้อยแล้ว!")
print(df.head(10))