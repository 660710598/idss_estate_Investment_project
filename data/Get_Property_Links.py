from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()

target_amount = 300
property_list = []
page = 1

print(f"เป้าหมาย: ดึงข้อมูลอสังหาฯ นครปฐม {target_amount} รายการ...")
while len(property_list) < target_amount:
    url = f"https://www.dotproperty.co.th/properties-for-sale/nakhon-pathom?page={page}"
    print(f"\nกำลังเปิดหน้า {page}...")
    driver.get(url)
    time.sleep(3) 

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        print("โหลดหน้าเว็บสำเร็จ! กำลังหาข้อมูล...")
    except:
        print("❌")
        break 

    # 🔍 ดึงข้อมูลอสังหาฯ ในหน้านี้ทั้งหมด
    articles = driver.find_elements(By.TAG_NAME, "article")
    if not articles:
        break

    for item in articles:
        if len(property_list) >= target_amount:
            break
            
        try:
            # 1. ดึงชื่อประกาศและลิงก์ 
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, "h3 a, h4 a")
            except:
                title_elem = item.find_element(By.TAG_NAME, "a")

            title = title_elem.text
            link = title_elem.get_attribute("href")
            
            if not title.strip():
                continue
                
            property_list.append({
                "ชื่อประกาศ": title, 
                "ลิงก์": link
            })
        except Exception as e:
            continue
            
    print(f"✅ ตอนนี้เก็บข้อมูลได้แล้ว {len(property_list)} / {target_amount} รายการ")
    page += 1 

df = pd.DataFrame(property_list)
df.to_csv("data/scraping/NakhonPathom_Properties.csv", index=False, encoding="utf-8-sig")
driver.quit()
print("เสร็จสิ้นการดึงข้อมูล!")