import pandas as pd

# โหลดไฟล์ CSV
file_path = "Effects of Violent Video Games.csv"

# โหลดข้อมูลจากไฟล์ CSV
df = pd.read_csv(file_path)

# ลบแถวที่มี Missing Values มากกว่า 50%
df = df.dropna(thresh=len(df.columns) * 0.5)

# ---------------------------- เติมค่าหายไปด้วยค่าที่เหมาะสม (เช่น 'Unknown' หรือ ค่ากลาง)
df = df.fillna("Unknown")

# ลบช่องว่างจากชื่อคอลัมน์
df.columns = df.columns.str.strip()

# ------------------------------------ แปลงค่าทุกคอลัมน์ให้เป็นตัวพิมพ์เล็ก (เฉพาะประเภทข้อความ)
df = df.applymap(lambda x: x.lower().strip() if isinstance(x, str) else x)

# ---------------------------- แก้ไขค่าที่สะกดผิด
df = df.replace({'niether disagree nor agree': 'neither agree nor disagree'})

# ------------------------------ แปลงคอลัมน์ที่เกี่ยวกับตัวเลขให้เป็นประเภทตัวเลข
num_cols = ['What is your age?']
df[num_cols] = df[num_cols].apply(pd.to_numeric, errors='coerce')

# ------------------------------- แทนที่ค่าที่หายไปในคอลัมน์อายุด้วยค่ามัธยฐาน (Median)
age_median = df['What is your age?'].median()
df['What is your age?'] = df['What is your age?'].fillna(age_median)

# แปลงคอลัมน์ที่เกี่ยวกับเวลาให้เป็น datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

# แทนค่าข้อมูลเวลาเล่นเกมรุนแรงให้เป็นตัวเลข
time_mapping = {
    "less than 1 hour": 0.5,
    "more than 1 hour": 1.5,
    "more than 2 hour": 2.5,
    "more than 3 hour": 3.5,
    "more than 5 hour": 5.5,
}

for col in df.columns:
    if df[col].astype(str).isin(time_mapping.keys()).any():  # ตรวจสอบว่ามีค่าเหล่านี้ในคอลัมน์หรือไม่
        df[col] = df[col].map(time_mapping)  # แปลงค่าในคอลัมน์นั้น

# -------------------------------- แปลงค่าความคิดเห็นให้เป็นตัวเลข
opinion_mapping = {
    'unknown' : 0,
    'strongly disagree': 1,
    'disagree': 2,
    'neither agree nor disagree': 3,
    'agree': 4,
    'strongly agree': 5
}
# ค้นหาคอลัมน์ที่เกี่ยวข้องกับความคิดเห็นแล้วแทนที่ค่าด้วยตัวเลข
opinion_cols = [col for col in df.columns if df[col].dtype == 'object' and df[col].isin(opinion_mapping.keys()).any()]
df[opinion_cols] = df[opinion_cols].applymap(lambda x: opinion_mapping.get(x, x))

# คำนวณคะแนนรวมของแต่ละแถว (เฉพาะคอลัมน์ที่เกี่ยวข้องกับความคิดเห็น)
df['Total Score'] = df[opinion_cols].sum(axis=1, numeric_only=True)

# ----------------------------- แบ่งคะแนนรวมตามเกณฑ์ที่กำหนด
def categorize_score(score):
    if 29 <= score <= 61:
        return 'Low'
    elif 62 <= score <= 76:
        return 'Average'
    elif 77 <= score <= 89:
        return 'Above Average'
    elif 90 <= score <= 100:
        return 'High'
    elif 101 <= score <= 149:
        return 'Very High'
    else:
        return 'Unknown'

df['Score Category'] = df['Total Score'].apply(categorize_score)
# นับความถี่ของแต่ละอายุ
age_counts = df['What is your age?'].value_counts()
print("Age Frequency Count:")
print(age_counts)

# -------------------------------- แบ่งประเภทเกม -------------------------

# คอลัมน์ที่ต้องใช้
game_column = "What type of video games do you typically play?"
hours_column = "How much time do you play \"violent\" video games specifically?"

# แปลงค่าเป็นตัวพิมพ์เล็กทั้งหมด
df[game_column] = df[game_column].astype(str).str.lower()

# -------------------------------- สร้างหมวดหมู่เกม -------------------------
game_categories = {
    "Action": ["action", "violent", "story driven action games"],
    "Shooter": ["first person shooter", "pubg", "free fire"],
    "Fighting": ["fighting"],
    "Sports/Racing": ["sports", "racing"],
    "Adventure/Open World": ["gta openworld", "red dead redemption", "the last of us"],
    "Puzzle/Casual": ["word connect", "puzzle", "cooking", "temple run"],
    "RPG": ["roleplay"]
}

# ฟังก์ชันจัดหมวดหมู่
game_types = ["Action", "Shooter", "Fighting", "Sports/Racing", "Adventure/Open World", "Puzzle/Casual", "RPG"]

# สร้างคอลัมน์ใหม่สำหรับแต่ละประเภทเกม
for game in game_types:
    df[game] = df["Game Category"].apply(lambda x: 1 if isinstance(x, str) and game in x else 0)

# # ใช้ฟังก์ชัน categorize_game กับข้อมูล
# df["Game Category"] = df[game_column].apply(categorize_game)

# ------------------------------------บันทึกไฟล์ที่ทำความสะอาดแล้ว----------------------------------
df.to_csv("cleaned_dataset_16.csv", index=False)

print("Data Cleaning Completed! File saved as cleaned_dataset.csv")

