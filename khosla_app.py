import streamlit as st
from PIL import Image
import pandas as pd
import os
import uuid
from datetime import datetime

# إعداد المجلدات
DATA_DIR = "images"
CSV_FILE = "data.csv"
os.makedirs(DATA_DIR, exist_ok=True)

# إعداد صفحة Streamlit
st.set_page_config(page_title="خصلة - AI صلع وراثي", layout="centered")
st.title("💇‍♂️ خصلة – التنبؤ بالصلع الوراثي")
st.markdown("يرجى ملء جميع البيانات ورفع **4 صور لفروة الرأس** (أمام، خلف، جانب أيسر، جانب أيمن).")

# --- 📌 البيانات الأساسية ---
st.header("البيانات الأساسية")
name = st.text_input("الاسم (اختياري)")
gender = st.selectbox("النوع", ["ذكر", "أنثى", "آخر"])
age = st.number_input("العمر", min_value=10, max_value=100, step=1)
country = st.text_input("الدولة / المنطقة")
hair_color = st.selectbox("لون الشعر الطبيعي", ["أسود", "بني", "أشقر", "أحمر", "أبيض/رمادي"])
hair_type = st.selectbox("نوع الشعر", ["ناعم", "متموج", "مجعد"])

# --- 📌 التاريخ العائلي ---
st.header("التاريخ العائلي")
family_history = st.radio("هل يوجد صلع وراثي في العائلة؟", ["نعم", "لا", "غير متأكد"])
relatives_with_baldness = st.multiselect(
    "إذا نعم، من أقارب الدرجة الأولى أو الثانية؟",
    ["الأب", "الأم", "الجد", "الجدة", "الأخ", "الأخت", "عم/خال", "عمة/خالة"]
)

# --- 📌 نمط الحياة ---
st.header("نمط الحياة")
stress_level = st.selectbox("معدل التوتر", ["منخفض", "متوسط", "عالي"])
sleep_hours = st.number_input("عدد ساعات النوم يوميًا", min_value=0, max_value=24, step=1)
diet_type = st.selectbox("النظام الغذائي", ["متوازن", "قليل البروتين", "غني بالدهون", "نباتي", "آخر"])
smoking = st.radio("هل تدخن؟", ["نعم", "لا"])
alcohol = st.radio("هل تتناول الكحول؟", ["نعم", "لا"])

# --- 📌 الصحة ---
st.header("الحالة الصحية")
chronic_diseases = st.text_area("أمراض مزمنة (إن وجدت)")
current_medications = st.text_area("أدوية حالية (إن وجدت)")
scalp_issues = st.text_area("مشاكل جلدية في فروة الرأس (إن وجدت)")

# --- 📸 الصور ---
st.header("الصور")
uploaded_files = st.file_uploader(
    "📌 ارفع 4 صور لشعرك من: الامام - الخلف - الجانب الايسر - الجانب الايمن",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    if len(uploaded_files) != 4:
        st.warning("⚠️ يجب رفع **4 صور فقط**.")
    else:
        st.success("✅ تم رفع 4 صور.")
        for i, file in enumerate(uploaded_files):
            st.image(Image.open(file), caption=f"الصورة رقم {i+1}", width=250)

# --- زر الإرسال ---
if st.button("✅ إرسال البيانات"):
    if len(uploaded_files) != 4:
        st.error("يرجى التأكد من رفع 4 صور.")
    else:
        # توليد ID فريد لكل مستخدم
        user_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:6]
        user_folder = os.path.join(DATA_DIR, user_id)
        os.makedirs(user_folder, exist_ok=True)

        # حفظ الصور
        for idx, file in enumerate(uploaded_files):
            image = Image.open(file)
            image_path = os.path.join(user_folder, f"image_{idx+1}.jpg")
            image.save(image_path)

        # حفظ البيانات
        new_data = {
            "user_id": user_id,
            "name": name,
            "gender": gender,
            "age": age,
            "country": country,
            "hair_color": hair_color,
            "hair_type": hair_type,
            "family_history": family_history,
            "relatives_with_baldness": ", ".join(relatives_with_baldness),
            "stress_level": stress_level,
            "sleep_hours": sleep_hours,
            "diet_type": diet_type,
            "smoking": smoking,
            "alcohol": alcohol,
            "chronic_diseases": chronic_diseases,
            "current_medications": current_medications,
            "scalp_issues": scalp_issues,
            "timestamp": datetime.now().isoformat()
        }

        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        else:
            df = pd.DataFrame([new_data])

        df.to_csv(CSV_FILE, index=False)
        st.success("✅ تم حفظ البيانات والصور بنجاح! شكراً لمشاركتك في مشروع خصلة.")


