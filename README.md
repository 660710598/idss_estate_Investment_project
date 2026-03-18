# ระบบช่วยตัดสินใจ (IDSS)

ระบบ IDSS สำหรับแนะนำการลงทุนอสังหาริมทรัพย์ (Real Estate Investment Decision Support System)

## โครงสร้างโปรเจค (คร่าวๆ)
- `app/` - โค้ดหลักของแอปพลิเคชัน
- `data/` - ข้อมูลตัวอย่างและข้อมูลนำเข้า
- `knowledge/` - กฎความรู้และไฟล์เกี่ยวกับกฎ (เช่น `city_plan_rules.py`, `expert_rules.json`)
- `model/` - โมดูลด้านโมเดล เช่น `decision_tree.py`, `financial_calc.py`

## วิธีติดตั้ง (จาก `requirements.txt`)

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

3. ข้อสังเกตสำหรับ Selenium:
- `selenium` ต้องการ WebDriver (เช่น ChromeDriver, geckodriver) เพื่อควบคุมเบราว์เซอร์ — ติดตั้งหรือตั้งค่าตัวจัดการไดร์เวอร์ตามเบราว์เซอร์ที่ใช้
- ถ้าใช้ Selenium 4.6+ ตัวจัดการไดร์เวอร์อาจช่วยดาวน์โหลดไดร์เวอร์ให้โดยอัตโนมัติ แต่ถ้าพบปัญหาให้ดาวน์โหลดไดร์เวอร์ที่ตรงกับเวอร์ชันเบราว์เซอร์แล้ววางไว้ใน PATH

4. ทดสอบการติดตั้ง (ตัวอย่าง):

```python
import pandas as pd
import numpy as np
import selenium
print('pandas', pd.__version__)
print('numpy', np.__version__)
print('selenium', selenium.__version__)
```
## ผู้จัดทำ
- 660710095 มโนรินทร์ นันทะนิ
- 660710598 เดชาธร ลายเขียน
- 660710623 ธนรัฐ จอมจุฑามาศ