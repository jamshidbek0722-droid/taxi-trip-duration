import streamlit as st
import pandas as pd
import joblib

model = joblib.load("model.pkl")

st.set_page_config(page_title="Taxi Trip Duration", page_icon="🚕", layout="wide")

# --- Session state ---
if "lang" not in st.session_state:
    st.session_state.lang = "🇺🇿 O'zbek"
dark = True

# --- Translations ---
T = {
    "🇺🇿 O'zbek": {
        "title": "🚕 Taxi Yo'l Vaqti Bashorati",
        "subtitle": "Kirish qiymatlarini bering — model yo'l vaqtini hisoblaydi.",
        "inputs": "⚙️ Kirish qiymatlari",
        "vendor": "Taksi kompaniyasi",
        "passengers": "Yo'lovchilar soni",
        "hour": "Soat",
        "weekday": "Hafta kuni",
        "weekday_help": "0 = Dushanba, 6 = Yakshanba",
        "month": "Oy",
        "night": "Tun vaqtimi? (22:00–06:00)",
        "distance": "Masofa (km)",
        "btn": "🔍 Bashorat qilish",
        "result": "🕒 Taxminiy yo'l vaqti",
        "min": "daqiqa", "sec": "soniya",
        "yes": "Ha", "no": "Yo'q",
        "contact": "📬 Muallif bilan bog'laning",
        "role": "ML Engineer",
        "model_info": "Model: XGBoost  |  Dataset: NYC Taxi 2016  |  R² = 0.761",
    },
    "🇷🇺 Русский": {
        "title": "🚕 Предсказание времени поездки",
        "subtitle": "Введите значения — модель рассчитает время поездки.",
        "inputs": "⚙️ Входные значения",
        "vendor": "Компания такси",
        "passengers": "Количество пассажиров",
        "hour": "Час",
        "weekday": "День недели",
        "weekday_help": "0 = Понедельник, 6 = Воскресенье",
        "month": "Месяц",
        "night": "Ночное время? (22:00–06:00)",
        "distance": "Расстояние (км)",
        "btn": "🔍 Предсказать",
        "result": "🕒 Примерное время поездки",
        "min": "мин", "sec": "сек",
        "yes": "Да", "no": "Нет",
        "contact": "📬 Связаться с автором",
        "role": "ML Engineer",
        "model_info": "Модель: XGBoost  |  Датасет: NYC Taxi 2016  |  R² = 0.761",
    },
    "🇬🇧 English": {
        "title": "🚕 Taxi Trip Duration Predictor",
        "subtitle": "Enter values and the model will predict the trip duration.",
        "inputs": "⚙️ Input Values",
        "vendor": "Taxi Vendor",
        "passengers": "Passenger Count",
        "hour": "Hour",
        "weekday": "Weekday",
        "weekday_help": "0 = Monday, 6 = Sunday",
        "month": "Month",
        "night": "Night time? (22:00–06:00)",
        "distance": "Distance (km)",
        "btn": "🔍 Predict",
        "result": "🕒 Estimated Trip Duration",
        "min": "min", "sec": "sec",
        "yes": "Yes", "no": "No",
        "contact": "📬 Contact the Author",
        "role": "ML Engineer",
        "model_info": "Model: XGBoost  |  Dataset: NYC Taxi 2016  |  R² = 0.761",
    }
}

WEEKDAYS = {
    "🇺🇿 O'zbek":  ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba","Yakshanba"],
    "🇷🇺 Русский": ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"],
    "🇬🇧 English": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
}

lang = st.session_state.lang
t = T[lang]

# --- Colors ---
if dark:
    BG, SIDE_BG, TEXT, SUB  = "#0e1117", "#161a23", "#f0f2f6", "#8b8fa8"
    CARD, BORDER, ACCENT     = "#1c2032", "#2a2d3e", "#00d4aa"
    BTN_TEXT = "#0e1117"
else:
    BG, SIDE_BG, TEXT, SUB  = "#f5f7fa", "#e8ebf2", "#1a1d2e", "#5a5f72"
    CARD, BORDER, ACCENT     = "#ffffff", "#d0d5e8", "#0055cc"
    BTN_TEXT = "#ffffff"

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] > .main {{ background-color: {BG}; }}
[data-testid="stSidebar"] > div:first-child {{ background-color: {SIDE_BG}; }}
[data-testid="stHeader"] {{ background-color: {BG}; }}
.stMarkdown p, [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
    color: {TEXT} !important;
}}
.stButton > button {{
    background: {ACCENT}; color: {BTN_TEXT};
    border: none; border-radius: 8px;
    padding: 12px 28px; font-size: 16px; font-weight: 700; width: 100%;
}}
.stButton > button:hover {{ opacity: 0.85; }}
.result-box {{
    background: {CARD}; border: 1px solid {BORDER};
    border-left: 5px solid {ACCENT}; border-radius: 12px; padding: 24px 28px; margin: 20px 0;
}}
.footer {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 14px;
    padding: 32px 20px; text-align: center; margin-top: 48px;
}}
.footer a {{
    color: {ACCENT} !important; text-decoration: none;
    font-weight: 600; margin: 0 14px; font-size: 15px;
}}
.footer a:hover {{ text-decoration: underline; }}
.stCaption p {{ color: {SUB} !important; }}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    new_lang = st.selectbox("🌐 Til / Язык / Language", list(T.keys()),
                             index=list(T.keys()).index(lang))
    if new_lang != lang:
        st.session_state.lang = new_lang
        st.rerun()

    st.divider()
    st.subheader(t["inputs"])

    vendor_id       = st.selectbox(t["vendor"], [1, 2], format_func=lambda x: f"Vendor {x}")
    passenger_count = st.slider(t["passengers"], 1, 6, 1)
    hour            = st.slider(t["hour"], 0, 23, 8)
    weekday         = st.slider(t["weekday"], 0, 6, 0, help=t["weekday_help"])
    month           = st.slider(t["month"], 1, 12, 1)
    night_val       = st.radio(t["night"], [0, 1],
                               format_func=lambda x: t["yes"] if x == 1 else t["no"],
                               horizontal=True)
    distance_km     = st.number_input(t["distance"], min_value=0.1, max_value=100.0,
                                      value=2.5, step=0.1)

# --- Main ---
st.title(t["title"])
st.markdown(f"<p style='color:{SUB}; font-size:16px; margin-bottom:24px;'>{t['subtitle']}</p>",
            unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric(f"🚕 {t['vendor']}",     f"Vendor {vendor_id}")
c2.metric(f"👥 {t['passengers']}", passenger_count)
c3.metric(f"📍 {t['distance']}",   f"{distance_km} km")
c4.metric(f"🕐 {t['hour']}",       f"{hour}:00")

c5, c6, c7 = st.columns(3)
c5.metric(f"📅 {t['weekday']}", WEEKDAYS[lang][weekday])
c6.metric(f"📆 {t['month']}",   month)
c7.metric(f"🌙 {t['night']}",   t["yes"] if night_val == 1 else t["no"])

st.divider()

if st.button(t["btn"]):
    input_df = pd.DataFrame([{
        "vendor_id":       vendor_id,
        "passenger_count": passenger_count,
        "hour":            hour,
        "weekday":         weekday,
        "month":           month,
        "night":           night_val,
        "distance_km":     distance_km,
    }])

    prediction = model.predict(input_df)[0]
    minutes    = int(prediction) // 60
    seconds    = int(prediction) % 60

    st.markdown(f"""
    <div class="result-box">
        <p style="color:{SUB}; margin:0 0 6px 0; font-size:14px;">{t['result']}</p>
        <h1 style="color:{ACCENT}; margin:0; font-size:52px;">
            {minutes} <span style="font-size:22px;">{t['min']}</span>
            &nbsp;{seconds} <span style="font-size:22px;">{t['sec']}</span>
        </h1>
    </div>
    """, unsafe_allow_html=True)

st.caption(t["model_info"])

# --- Footer ---
st.markdown(f"""
<div class="footer">
    <p style="color:{SUB}; font-size:13px; margin:0 0 4px 0;">{t['contact']}</p>
    <h2 style="color:{TEXT}; margin:0 0 2px 0;">Jamshid Erkinov</h2>
    <p style="color:{ACCENT}; font-weight:700; font-size:15px; margin:0 0 20px 0;">{t['role']}</p>
    <div>
        <a href="https://t.me/Jamshidbek0722" target="_blank">✈️ Telegram</a>
        <a href="mailto:jamshidbek.0722@gmail.com">📧 Gmail</a>
        <a href="https://github.com/jamshidbek0722-droid" target="_blank">🐙 GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)
