import pandas as pd

# โหลดข้อมูลจากไฟล์ (ใส่ path ไฟล์จริง)
df = pd.read_csv('data/cleaned_dataset_17.csv')

# ตรวจสอบข้อมูลเบื้องต้น
print("จำนวนข้อมูลทั้งหมด:", len(df))

# สุ่มกลุ่มตัวอย่าง 60 คน
sample_df = df.sample(n=60, random_state=42)  # ใช้ random_state เพื่อให้ผล reproducible

# ตรวจสอบตัวอย่างข้อมูล
print(sample_df.head())

# บันทึกเป็นไฟล์ใหม่ (ถ้าอยากเอาไปใช้ต่อ เช่น สำหรับ SPSS หรือ Excel)
sample_df.to_csv("sample60c.csv", index=False)
