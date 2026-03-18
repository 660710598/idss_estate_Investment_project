# ระบบช่วยตัดสินใจ (IDSS)

ระบบ IDSS สำหรับแนะนำการลงทุนอสังหาริมทรัพย์ (Real Estate Investment Decision Support System)

## โครงสร้างโปรเจค (คร่าวๆ)
- `app/` - โค้ดหลักของแอปพลิเคชัน
- `data/` - ข้อมูลตัวอย่างและข้อมูลนำเข้า
- `knowledge/` - กฎความรู้และไฟล์เกี่ยวกับกฎ (เช่น `city_plan_rules.py`, `expert_rules.json`)
- `model/` - โมดูลด้านโมเดล เช่น `decision_tree.py`, `financial_calc.py`

## วิธีติดตั้ง และรันโปรเจค (Quick Start)

1. สร้าง virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

หากใช้ Command Prompt:

```cmd
python -m venv .venv
.\.venv\Scripts\activate
```

2. อัพเกรด pip แล้วติดตั้งแพ็กเกจจากไฟล์ `requirements.txt`:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. WebDriver / Selenium:
- สคริปต์ `data/scraping/Get_Property_Links.py` ใช้ `selenium` + เบราว์เซอร์ (เช่น Chrome). ต้องมี WebDriver (เช่น ChromeDriver) ที่ตรงกับเวอร์ชันเบราว์เซอร์ และอยู่ใน `PATH`.
- ทางเลือก: ติดตั้ง `webdriver-manager` (รวมไว้ใน `requirements.txt`) และปรับสคริปต์ให้ใช้ `webdriver_manager.chrome import ChromeDriverManager` เพื่อดาวน์โหลดไดร์เวอร์อัตโนมัติ.

4. คำสั่งรันสำคัญ (ตัวอย่าง):

- ดึงลิงก์ประกาศ (scraper):

```powershell
python data/scraping/Get_Property_Links.py
```

- ทำความสะอาดข้อมูลและสร้างไฟล์ CSV ที่ใช้โดยแอป:

```powershell
python data/scraping/Cleaning.py
```

- รันแอป Streamlit (UI):

```powershell
streamlit run app/main.py
```

5. ทดสอบการติดตั้ง (ตัวอย่างเล็กน้อย):

```python
import pandas as pd
import numpy as np
import selenium
import streamlit
print('pandas', pd.__version__)
print('numpy', np.__version__)
print('selenium', selenium.__version__)
print('streamlit', streamlit.__version__)
```
## ผู้จัดทำ
- 660710095 มโนรินทร์ นันทะนิ
- 660710598 เดชาธร ลายเขียน
- 660710623 ธนรัฐ จอมจุฑามาศ