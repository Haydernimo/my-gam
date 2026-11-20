import streamlit as st
from streamlit_autorefresh import st_autorefresh
import sqlite3
import random
import json
import time
from pathlib import Path
from datetime import datetime

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "quiz_master.db"

st.set_page_config(
    page_title="Quiz Master | اختبر معلوماتك",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- Bilingual interface --------------------
TEXT = {
    "en": {
        "home": "Home", "leaderboard": "Leaderboard", "admin": "Admin Panel",
        "about": "About", "about_desc": "A Python-powered quiz platform built with Streamlit and SQLite.",
        "tagline": "KNOWLEDGE • CHALLENGE • GROW",
        "hero_eyebrow": "THE KNOWLEDGE ARENA",
        "hero_title": "Challenge your mind.<br>Discover what you know.",
        "hero_desc": "Choose a category, answer the questions, and climb the leaderboard.",
        "questions_bank": "QUESTIONS IN BANK", "completed": "QUIZZES COMPLETED",
        "average": "AVERAGE SCORE", "explore": "Explore categories",
        "your_name": "Your name", "name_placeholder": "Enter your name to appear on the leaderboard",
        "start": "Start", "question_count": "questions", "timer_info": "Each question has 20 seconds. Your result is saved locally in this app.",
        "challenge": "challenge", "player": "Player", "question": "Question",
        "time_left": "TIME LEFT", "choose": "Choose your answer",
        "confirm": "Confirm answer", "select_warning": "Please select an answer first.",
        "timer_caption": "The countdown updates every second. Select an answer, then confirm.",
        "expired": "Time is up! Moving to the next question…",
        "performance": "YOUR PERFORMANCE", "completed_title": "Quiz completed!",
        "completed_desc": "Every question is a chance to learn something new.",
        "score": "YOUR SCORE", "accuracy": "ACCURACY", "category": "CATEGORY",
        "excellent": "Outstanding performance! You really know your stuff.",
        "good": "Good effort! Keep practicing to improve your score.",
        "keep_learning": "Keep learning. Every attempt makes you better.",
        "review": "Answer review", "your_answer": "Your answer",
        "correct_answer": "Correct answer", "no_answer": "Time expired / No answer",
        "play_again": "Play another quiz", "view_leaderboard": "View leaderboard",
        "leaderboard_title": "Leaderboard", "leaderboard_desc": "Top quiz performances saved in this app.",
        "no_results": "No results yet. Complete a quiz to appear here.",
        "back_home": "Back to home", "admin_title": "Admin panel",
        "admin_desc": "Manage the question bank stored in the local SQLite database.",
        "add_question": "Add a new question", "question_en": "Question (English)",
        "question_ar": "Question (Arabic)", "option_en": "Option", "option_ar": "Arabic option",
        "correct": "Correct answer", "explanation_en": "Explanation (English, optional)",
        "explanation_ar": "Explanation (Arabic, optional)", "save_question": "Save question",
        "fill_fields": "Please enter the question and all four options in both languages.",
        "saved": "Question added successfully.", "existing": "Existing questions",
        "filter": "Filter by category", "all_categories": "All categories",
        "delete": "Delete", "shown": "Total questions shown",
        "guest": "Guest", "language": "Language", "arabic": "العربية",
        "english": "English", "switch_hint": "Choose the interface language.",
        "no_questions": "No questions are available in this category yet.",
        "question_number": "QUESTION",
    },
    "ar": {
        "home": "الرئيسية", "leaderboard": "لوحة المتصدرين", "admin": "لوحة الإدارة",
        "about": "حول التطبيق", "about_desc": "منصة مسابقات معرفية مبنية باستخدام Python وStreamlit وSQLite.",
        "tagline": "معرفة • تحدٍّ • تطوّر",
        "hero_eyebrow": "ساحة المعرفة",
        "hero_title": "تحدَّ عقلك.<br>واكتشف مقدار معرفتك.",
        "hero_desc": "اختر تصنيفاً، وأجب عن الأسئلة، وتقدّم في لوحة المتصدرين.",
        "questions_bank": "عدد الأسئلة", "completed": "المسابقات المكتملة",
        "average": "معدل النتائج", "explore": "استكشف التصنيفات",
        "your_name": "اسم اللاعب", "name_placeholder": "أدخل اسمك ليظهر في لوحة المتصدرين",
        "start": "ابدأ", "question_count": "سؤالاً", "timer_info": "لديك 20 ثانية لكل سؤال، وستُحفظ نتيجتك داخل التطبيق.",
        "challenge": "مسابقة", "player": "اللاعب", "question": "السؤال",
        "time_left": "الوقت المتبقي", "choose": "اختر إجابتك",
        "confirm": "تأكيد الإجابة", "select_warning": "يرجى اختيار إجابة أولاً.",
        "timer_caption": "يتحدّث العدّ التنازلي كل ثانية. اختر إجابة ثم اضغط تأكيد الإجابة.",
        "expired": "انتهى الوقت! جارٍ الانتقال إلى السؤال التالي…",
        "performance": "أداؤك", "completed_title": "اكتملت المسابقة!",
        "completed_desc": "كل سؤال فرصة لاكتساب معرفة جديدة.",
        "score": "نتيجتك", "accuracy": "نسبة الإجابات الصحيحة", "category": "التصنيف",
        "excellent": "أداء رائع! لديك حصيلة معرفية مميزة.",
        "good": "أحسنت! واصل التدريب لتحسين نتيجتك.",
        "keep_learning": "واصل التعلم، فكل محاولة تجعلك أفضل.",
        "review": "مراجعة الإجابات", "your_answer": "إجابتك",
        "correct_answer": "الإجابة الصحيحة", "no_answer": "انتهى الوقت / لم تتم الإجابة",
        "play_again": "ابدأ مسابقة جديدة", "view_leaderboard": "عرض لوحة المتصدرين",
        "leaderboard_title": "لوحة المتصدرين", "leaderboard_desc": "أفضل نتائج المسابقات المسجلة في التطبيق.",
        "no_results": "لا توجد نتائج حتى الآن. أكمل مسابقة لتظهر هنا.",
        "back_home": "العودة للرئيسية", "admin_title": "لوحة الإدارة",
        "admin_desc": "إدارة بنك الأسئلة المحفوظ في قاعدة بيانات SQLite المحلية.",
        "add_question": "إضافة سؤال جديد", "question_en": "السؤال (بالإنجليزية)",
        "question_ar": "السؤال (بالعربية)", "option_en": "الخيار", "option_ar": "الخيار بالعربية",
        "correct": "الإجابة الصحيحة", "explanation_en": "التوضيح (بالإنجليزية - اختياري)",
        "explanation_ar": "التوضيح (بالعربية - اختياري)", "save_question": "حفظ السؤال",
        "fill_fields": "يرجى إدخال السؤال والخيارات الأربعة باللغتين.",
        "saved": "تمت إضافة السؤال بنجاح.", "existing": "الأسئلة الموجودة",
        "filter": "تصفية حسب التصنيف", "all_categories": "كل التصنيفات",
        "delete": "حذف", "shown": "عدد الأسئلة المعروضة",
        "guest": "زائر", "language": "اللغة", "arabic": "العربية",
        "english": "English", "switch_hint": "اختر لغة واجهة التطبيق.",
        "no_questions": "لا توجد أسئلة متاحة في هذا التصنيف حالياً.",
        "question_number": "السؤال",
    },
}

CATEGORIES = {
    "General Knowledge": ("🌟", "معلومات عامة", "A little bit of everything", "منوعات في شتى المجالات"),
    "History": ("🏛️", "التاريخ", "Civilizations, leaders and events", "الحضارات والقادة والأحداث"),
    "Science": ("🔬", "العلوم", "Discover the world around you", "اكتشف العالم من حولك"),
    "Geography": ("🌍", "الجغرافيا", "Countries, capitals and nature", "الدول والعواصم والطبيعة"),
    "Iraqi Heritage": ("𒀭", "تراث العراق", "Mesopotamia and ancient Iraq", "بلاد الرافدين والعراق القديم"),
}
CAT_AR_TO_EN = {v[1]: k for k, v in CATEGORIES.items()}

# Each question stores English and Arabic wording. Existing database entries
# from earlier versions are also supported (they simply fall back to English).
SEED_QUESTIONS = [
    ("General Knowledge", "Which language is primarily used with the Streamlit framework?", "ما لغة البرمجة الأساسية المستخدمة مع إطار Streamlit؟", ["Python", "Java", "C++", "Dart"], ["بايثون", "جافا", "سي بلس بلس", "دارت"], 0, "Streamlit apps are written in Python.", "تُكتب تطبيقات Streamlit باستخدام لغة بايثون."),
    ("General Knowledge", "How many days are there in a leap year?", "كم يوماً توجد في السنة الكبيسة؟", ["364", "365", "366", "367"], ["364", "365", "366", "367"], 2, "A leap year has 366 days.", "تحتوي السنة الكبيسة على 366 يوماً."),
    ("General Knowledge", "Which is the largest mammal on Earth?", "ما أكبر الثدييات حجماً على الأرض؟", ["African elephant", "Blue whale", "Giraffe", "Orca"], ["الفيل الأفريقي", "الحوت الأزرق", "الزرافة", "الأوركا"], 1, "The blue whale is the largest known animal.", "الحوت الأزرق هو أكبر حيوان معروف."),
    ("General Knowledge", "What is the main currency of Japan?", "ما العملة الرسمية لليابان؟", ["Won", "Yuan", "Yen", "Ringgit"], ["الوون", "اليوان", "الين", "الرينغيت"], 2, "Japan's currency is the yen.", "عملة اليابان هي الين."),
    ("History", "Which civilization developed in southern Mesopotamia?", "أي حضارة نشأت في جنوب بلاد الرافدين؟", ["Sumerian", "Mayan", "Aztec", "Phoenician"], ["السومرية", "المايا", "الأزتك", "الفينيقية"], 0, "Sumerian city-states developed in southern Mesopotamia.", "نشأت دويلات المدن السومرية في جنوب بلاد الرافدين."),
    ("History", "Who was the first emperor of Rome?", "من كان أول إمبراطور لروما؟", ["Julius Caesar", "Augustus", "Nero", "Trajan"], ["يوليوس قيصر", "أغسطس", "نيرون", "تراجان"], 1, "Augustus became the first Roman emperor.", "أصبح أغسطس أول إمبراطور روماني."),
    ("History", "The ancient city of Babylon was located in which modern country?", "في أي دولة حديثة تقع مدينة بابل الأثرية؟", ["Egypt", "Iraq", "Turkey", "Iran"], ["مصر", "العراق", "تركيا", "إيران"], 1, "Babylon was located in present-day Iraq.", "تقع بابل في العراق حالياً."),
    ("History", "Which ancient civilization built the city of Persepolis?", "أي حضارة قديمة بنت مدينة برسيبوليس؟", ["Assyrian", "Persian", "Greek", "Roman"], ["الآشورية", "الفارسية", "اليونانية", "الرومانية"], 1, "Persepolis was a ceremonial capital of the Achaemenid Persian Empire.", "كانت برسيبوليس عاصمة احتفالية للإمبراطورية الأخمينية الفارسية."),
    ("Science", "What is the chemical formula for water?", "ما الصيغة الكيميائية للماء؟", ["CO2", "O2", "H2O", "NaCl"], ["CO2", "O2", "H2O", "NaCl"], 2, "A water molecule contains two hydrogen atoms and one oxygen atom.", "يتكون جزيء الماء من ذرتي هيدروجين وذرة أكسجين."),
    ("Science", "Which planet is known as the Red Planet?", "أي كوكب يُعرف بالكوكب الأحمر؟", ["Venus", "Mars", "Jupiter", "Mercury"], ["الزهرة", "المريخ", "المشتري", "عطارد"], 1, "Iron oxide gives Mars its reddish appearance.", "يمنح أكسيد الحديد المريخ لونه المحمر."),
    ("Science", "What is the approximate speed of light in a vacuum?", "ما السرعة التقريبية للضوء في الفراغ؟", ["300,000 km/s", "30,000 km/s", "3,000 km/s", "3 million km/s"], ["300,000 كم/ث", "30,000 كم/ث", "3,000 كم/ث", "3 ملايين كم/ث"], 0, "Light travels at about 299,792 kilometers per second.", "تبلغ سرعة الضوء نحو 299,792 كيلومتراً في الثانية."),
    ("Science", "Which organ pumps blood around the human body?", "أي عضو يضخ الدم في جسم الإنسان؟", ["Liver", "Lungs", "Heart", "Kidney"], ["الكبد", "الرئتان", "القلب", "الكلية"], 2, "The heart circulates blood through the body.", "يضخ القلب الدم إلى أنحاء الجسم."),
    ("Geography", "What is the largest ocean on Earth?", "ما أكبر محيط على سطح الأرض؟", ["Atlantic", "Indian", "Arctic", "Pacific"], ["الأطلسي", "الهندي", "المتجمد الشمالي", "الهادئ"], 3, "The Pacific Ocean is the largest and deepest ocean.", "المحيط الهادئ هو أكبر المحيطات وأعمقها."),
    ("Geography", "What is the capital of Japan?", "ما عاصمة اليابان؟", ["Kyoto", "Tokyo", "Osaka", "Nagoya"], ["كيوتو", "طوكيو", "أوساكا", "ناغويا"], 1, "Tokyo is Japan's capital.", "طوكيو هي عاصمة اليابان."),
    ("Geography", "On which continent is the Sahara Desert?", "في أي قارة تقع الصحراء الكبرى؟", ["Asia", "Africa", "South America", "Australia"], ["آسيا", "أفريقيا", "أمريكا الجنوبية", "أستراليا"], 1, "The Sahara stretches across North Africa.", "تمتد الصحراء الكبرى عبر شمال أفريقيا."),
    ("Geography", "Which river flows through Baghdad?", "أي نهر يمر بمدينة بغداد؟", ["Nile", "Euphrates", "Tigris", "Jordan"], ["النيل", "الفرات", "دجلة", "الأردن"], 2, "Baghdad stands on the Tigris River.", "تقع بغداد على ضفاف نهر دجلة."),
    ("Iraqi Heritage", "Which writing system was widely used by the Sumerians?", "ما نظام الكتابة الذي استخدمه السومريون على نطاق واسع؟", ["Hieroglyphs", "Cuneiform", "Latin", "Sanskrit"], ["الهيروغليفية", "المسمارية", "اللاتينية", "السنسكريتية"], 1, "Cuneiform was impressed into clay tablets.", "كانت الكتابة المسمارية تُنقش على الألواح الطينية."),
    ("Iraqi Heritage", "What was the famous law code associated with Babylonian king Hammurabi?", "ما اسم مجموعة القوانين الشهيرة المرتبطة بالملك البابلي حمورابي؟", ["Twelve Tables", "Code of Hammurabi", "Justinian Code", "Ur-Nammu Edict"], ["الألواح الاثنا عشر", "شريعة حمورابي", "قانون جستنيان", "قانون أور نمو"], 1, "The Code of Hammurabi is one of the best-known ancient law collections.", "تُعد شريعة حمورابي من أشهر مجموعات القوانين القديمة."),
    ("Iraqi Heritage", "Which ancient city is strongly associated with the Assyrian Empire?", "أي مدينة قديمة ارتبطت بقوة بالإمبراطورية الآشورية؟", ["Nineveh", "Athens", "Memphis", "Sparta"], ["نينوى", "أثينا", "منف", "إسبرطة"], 0, "Nineveh was a major Assyrian capital.", "كانت نينوى إحدى العواصم الآشورية المهمة."),
    ("Iraqi Heritage", "The Epic of Gilgamesh originated in which region?", "في أي منطقة نشأت ملحمة جلجامش؟", ["Mesopotamia", "Scandinavia", "China", "Greece"], ["بلاد الرافدين", "إسكندنافيا", "الصين", "اليونان"], 0, "The epic originated in ancient Mesopotamia.", "نشأت الملحمة في بلاد الرافدين القديمة."),
]

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_index INTEGER NOT NULL,
            explanation TEXT DEFAULT ''
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percent INTEGER NOT NULL,
            played_at TEXT NOT NULL
        )""")
        count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        if count == 0:
            conn.executemany(
                """INSERT INTO questions(category,question,options,correct_index,explanation)
                   VALUES(?,?,?,?,?)""",
                [(c, q_en + "||| " + q_ar,
                  json.dumps([a + "|||" + b for a, b in zip(opts_en, opts_ar)], ensure_ascii=False),
                  correct, exp_en + "||| " + exp_ar)
                 for c, q_en, q_ar, opts_en, opts_ar, correct, exp_en, exp_ar in SEED_QUESTIONS]
            )
        # Upgrade questions created by the earlier English-only version.
        for item in SEED_QUESTIONS:
            c, q_en, q_ar, opts_en, opts_ar, correct, exp_en, exp_ar = item
            old = conn.execute(
                "SELECT id FROM questions WHERE category=? AND question=?",
                (c, q_en)
            ).fetchone()
            if old:
                bilingual_options = [a + "||| " + b for a, b in zip(opts_en, opts_ar)]
                conn.execute(
                    "UPDATE questions SET question=?, options=?, explanation=? WHERE id=?",
                    (q_en + "||| " + q_ar,
                     json.dumps(bilingual_options, ensure_ascii=False),
                     exp_en + "||| " + exp_ar, old["id"])
                )
        conn.commit()

def localized(value, lang):
    """Read bilingual fields separated by |||; keep compatibility with old rows."""
    if value is None:
        return ""
    parts = str(value).split("|||", 1)
    if len(parts) == 1:
        return parts[0].strip()
    return (parts[1] if lang == "ar" else parts[0]).strip()

def get_questions(category):
    with connect() as conn:
        rows = conn.execute("SELECT * FROM questions WHERE category=? ORDER BY id", (category,)).fetchall()
    result = []
    for row in rows:
        raw_options = json.loads(row["options"])
        result.append({
            "id": row["id"], "category": row["category"],
            "question": row["question"], "options": raw_options,
            "correct_index": row["correct_index"], "explanation": row["explanation"] or ""
        })
    return result

def save_result(player, category, score, total):
    percent = round(score / total * 100) if total else 0
    with connect() as conn:
        conn.execute(
            "INSERT INTO results(player,category,score,total,percent,played_at) VALUES(?,?,?,?,?,?)",
            (player, category, score, total, percent, datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()

def get_leaderboard(limit=50):
    with connect() as conn:
        return conn.execute(
            """SELECT player,category,score,total,percent,played_at FROM results
               ORDER BY percent DESC,score DESC,id DESC LIMIT ?""", (limit,)
        ).fetchall()

def get_stats():
    with connect() as conn:
        q_count = conn.execute("SELECT COUNT(*) FROM questions").fetchone()[0]
        r_count = conn.execute("SELECT COUNT(*) FROM results").fetchone()[0]
        avg = conn.execute("SELECT AVG(percent) FROM results").fetchone()[0]
    return q_count, r_count, round(avg or 0)

init_db()

if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "page" not in st.session_state:
    st.session_state.page = "home"
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None

lang = st.session_state.lang
t = TEXT[lang]
rtl = lang == "ar"

# -------------------- Styling --------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cairo:wght@400;500;600;700;800&display=swap');
:root {{ --bg:#0b1020; --panel:#141c32; --purple:#8067f2; --gold:#f4c76b; }}
.stApp {{ background:radial-gradient(circle at 80% 0%,#22204b 0,#0b1020 42%,#0b1020 100%); color:#f4f6ff; }}
html,body,[class*="css"] {{ font-family:{("'Cairo','Inter'" if rtl else "'Inter','Cairo'")},sans-serif; }}
.block-container {{ max-width:1200px; padding-top:1.5rem; padding-bottom:3rem; }}
[data-testid="stSidebar"] {{ background:#10182b; border-right:1px solid #26314e; }}
.hero {{ padding:2.2rem; border-radius:24px; background:linear-gradient(120deg,#34266e 0%,#624bd0 55%,#283a70 100%); border:1px solid #7563d8; box-shadow:0 18px 50px #0005; direction:{'rtl' if rtl else 'ltr'}; text-align:{'right' if rtl else 'left'}; }}
.hero h1 {{ font-size:2.35rem; line-height:1.35; margin:0; color:white; font-weight:800; }}
.hero p {{ color:#e0dcff; font-size:1.05rem; margin:.7rem 0 0 0; }}
.eyebrow {{ color:#f5d78d; text-transform:uppercase; letter-spacing:1px; font-size:.75rem; font-weight:800; }}
.section-title {{ font-size:1.35rem; font-weight:800; margin:1.4rem 0 .8rem; }}
.metric-card,.category-card {{ background:linear-gradient(145deg,#18223b,#121a2e); border:1px solid #2b385a; border-radius:18px; padding:1.1rem 1.25rem; min-height:112px; direction:{'rtl' if rtl else 'ltr'}; text-align:{'right' if rtl else 'left'}; }}
.metric-label,.small-muted {{ color:#aab5d0; font-size:.88rem; }}
.metric-value {{ font-size:1.8rem; font-weight:800; color:white; margin-top:.3rem; }}
.category-icon {{ font-size:1.8rem; }}
.category-name {{ font-weight:800; font-size:1.05rem; margin-top:.5rem; }}
.category-desc {{ color:#aab5d0; font-size:.82rem; margin-top:.25rem; }}
.question-box {{ background:linear-gradient(145deg,#1b2745,#141c32); border:1px solid #36446b; border-radius:20px; padding:1.5rem; margin:.8rem 0 1.2rem; direction:{'rtl' if rtl else 'ltr'}; text-align:{'right' if rtl else 'left'}; }}
div.stButton > button {{ border-radius:12px; font-weight:700; min-height:2.8rem; border:1px solid #5c4bb4; }}
div.stButton > button[kind="primary"] {{ background:linear-gradient(90deg,#7257e8,#9279ff); border:0; color:white; }}
div[data-testid="stMetric"] {{ background:#151f36; border:1px solid #2b385a; padding:1rem; border-radius:16px; }}
[data-testid="stRadio"] {{ direction:{'rtl' if rtl else 'ltr'}; text-align:{'right' if rtl else 'left'}; }}
[data-testid="stMarkdownContainer"] {{ direction:{'rtl' if rtl else 'ltr'}; }}
input,textarea {{ text-align:{'right' if rtl else 'left'}; }}
hr {{ border-color:#283452; }}
footer {{ visibility:hidden; }}
</style>
""", unsafe_allow_html=True)

def go(page):
    st.session_state.page = page
    st.rerun()

def start_quiz(category, player, amount=10):
    bank = get_questions(category)
    if not bank:
        st.warning(t["no_questions"])
        return
    random.shuffle(bank)
    bank = bank[:min(amount, len(bank))]
    st.session_state.quiz = {
        "category": category, "player": player.strip() or t["guest"],
        "questions": bank, "index": 0, "answers": [],
        "started": time.time(), "question_started": time.time(), "duration": 20,
        "selected": None,
    }
    go("quiz")

def finish_quiz():
    quiz = st.session_state.quiz
    score = sum(1 for i, q in enumerate(quiz["questions"])
                if quiz["answers"][i] == q["correct_index"])
    total = len(quiz["questions"])
    save_result(quiz["player"], quiz["category"], score, total)
    st.session_state.last_result = {
        "player": quiz["player"], "category": quiz["category"],
        "score": score, "total": total,
        "answers": list(quiz["answers"]), "questions": list(quiz["questions"]),
    }
    st.session_state.quiz = None
    go("result")

def advance_question(answer):
    quiz = st.session_state.quiz
    quiz["answers"].append(answer)
    if quiz["index"] + 1 >= len(quiz["questions"]):
        finish_quiz()
    else:
        quiz["index"] += 1
        quiz["question_started"] = time.time()
        quiz["selected"] = None
        go("quiz")

def category_name(category):
    return CATEGORIES[category][1] if lang == "ar" else category

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 🧠 Quiz Master")
    st.caption(t["tagline"])
    st.divider()
    st.selectbox(
        t["language"], options=["en", "ar"],
        format_func=lambda x: t["english"] if x == "en" else t["arabic"],
        index=0 if lang == "en" else 1, key="language_selector"
    )
    if st.session_state.language_selector != st.session_state.lang:
        st.session_state.lang = st.session_state.language_selector
        st.rerun()
    st.divider()
    if st.button("🏠  " + t["home"], use_container_width=True):
        go("home")
    if st.button("🏆  " + t["leaderboard"], use_container_width=True):
        go("leaderboard")
    if st.button("⚙️  " + t["admin"], use_container_width=True):
        go("admin")
    st.divider()
    st.markdown("**" + t["about"] + "**")
    st.caption(t["about_desc"])
    st.caption("Version 2.0 • SQLite")

# -------------------- Home --------------------
if st.session_state.page == "home":
    q_count, r_count, avg = get_stats()
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">{t['hero_eyebrow']}</div>
      <h1>{t['hero_title']}</h1>
      <p>{t['hero_desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, label, value in [
        (c1, t["questions_bank"], q_count),
        (c2, t["completed"], r_count),
        (c3, t["average"], f"{avg}%"),
    ]:
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div></div>', unsafe_allow_html=True
            )
    st.markdown('<div class="section-title">' + t["explore"] + '</div>', unsafe_allow_html=True)
    name = st.text_input(t["your_name"], placeholder=t["name_placeholder"])
    cols = st.columns(2)
    for i, (category, details) in enumerate(CATEGORIES.items()):
        emoji, ar_name, en_desc, ar_desc = details
        with cols[i % 2]:
            count = len(get_questions(category))
            shown_name = ar_name if lang == "ar" else category
            desc = ar_desc if lang == "ar" else en_desc
            st.markdown(f"""
            <div class="category-card">
              <div class="category-icon">{emoji}</div>
              <div class="category-name">{shown_name}</div>
              <div class="category-desc">{desc} • {count} {t['question_count']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{t['start']} {shown_name} ←" if rtl else f"{t['start']} {shown_name} →",
                         key=f"start_{category}", use_container_width=True):
                start_quiz(category, name, 10)
    st.info(t["timer_info"])

# -------------------- Quiz --------------------
elif st.session_state.page == "quiz":
    quiz = st.session_state.quiz
    if not quiz:
        go("home")
    else:
        # Refresh every second; the selected answer is stored in quiz state.
        st_autorefresh(interval=1000, key=f"quiz_timer_{quiz['index']}")
        idx = quiz["index"]
        q = quiz["questions"][idx]
        elapsed = time.time() - quiz["question_started"]
        remaining = max(0, quiz["duration"] - int(elapsed))
        if remaining <= 0:
            st.warning(t["expired"])
            advance_question(-1)
            st.stop()

        display_question = localized(q["question"], lang)
        display_options = [localized(option, lang) for option in q["options"]]
        st.markdown(f"### {category_name(quiz['category'])} {t['challenge']}")
        st.caption(f"{t['player']}: {quiz['player']}  •  {t['question']} {idx+1} / {len(quiz['questions'])}")
        st.progress((idx + 1) / len(quiz["questions"]))
        m1, m2 = st.columns(2)
        m1.metric(t["question_number"], f"{idx+1}/{len(quiz['questions'])}")
        m2.metric(t["time_left"], f"{remaining}s")
        st.markdown(
            f'<div class="question-box"><div class="eyebrow">{t["question_number"]} {idx+1:02d}</div>'
            f'<h2>{display_question}</h2></div>', unsafe_allow_html=True
        )

        # Button-based answers: selected index is saved in quiz state across reruns.
        st.write(t["choose"])
        selected = quiz.get("selected")
        for option_index, option_text in enumerate(display_options):
            label = ("✓  " if selected == option_index else "○  ") + option_text
            if st.button(label, key=f"answer_button_{idx}_{option_index}",
                         type="primary" if selected == option_index else "secondary",
                         use_container_width=True):
                quiz["selected"] = option_index
                st.rerun()

        if st.button(t["confirm"] + (" ←" if rtl else " →"),
                     type="primary", use_container_width=True, key=f"confirm_{idx}"):
            selected = quiz.get("selected")
            if selected is None:
                st.warning(t["select_warning"])
            elif time.time() - quiz["question_started"] >= quiz["duration"]:
                st.warning(t["expired"])
                advance_question(-1)
            else:
                advance_question(selected)
        st.caption(t["timer_caption"])

# -------------------- Result --------------------
elif st.session_state.page == "result":
    result = st.session_state.last_result
    if not result:
        go("home")
    else:
        score, total = result["score"], result["total"]
        pct = round(score / total * 100) if total else 0
        st.markdown(
            f'<div class="hero"><div class="eyebrow">{t["performance"]}</div>'
            f'<h1>{t["completed_title"]}</h1><p>{t["completed_desc"]}</p></div>',
            unsafe_allow_html=True
        )
        a, b, c = st.columns(3)
        a.metric(t["score"], f"{score}/{total}")
        b.metric(t["accuracy"], f"{pct}%")
        c.metric(t["category"], category_name(result["category"]))
        if pct >= 80:
            st.success(t["excellent"])
        elif pct >= 50:
            st.info(t["good"])
        else:
            st.warning(t["keep_learning"])
        st.markdown("### " + t["review"])
        for i, q in enumerate(result["questions"]):
            chosen = result["answers"][i]
            correct = q["correct_index"]
            question_text = localized(q["question"], lang)
            with st.expander(f"{'✅' if chosen == correct else '❌'}  {i+1}. {question_text}"):
                options = [localized(option, lang) for option in q["options"]]
                st.write(f"**{t['your_answer']}:** {options[chosen] if chosen >= 0 else t['no_answer']}")
                st.write(f"**{t['correct_answer']}:** {options[correct]}")
                explanation = localized(q["explanation"], lang)
                if explanation:
                    st.caption(explanation)
        left, right = st.columns(2)
        with left:
            if st.button(t["play_again"], type="primary", use_container_width=True):
                go("home")
        with right:
            if st.button(t["view_leaderboard"], use_container_width=True):
                go("leaderboard")

# -------------------- Leaderboard --------------------
elif st.session_state.page == "leaderboard":
    st.markdown("## 🏆 " + t["leaderboard_title"])
    st.caption(t["leaderboard_desc"])
    rows = get_leaderboard(50)
    if not rows:
        st.info(t["no_results"])
    else:
        for i, row in enumerate(rows, start=1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            st.markdown(f"""
            <div class="category-card" style="min-height:unset;margin-bottom:.6rem;padding:.9rem 1.2rem;">
              <b>{medal} &nbsp; {row['player']}</b>
              <span style="float:right;color:#f4c76b;font-weight:800;">{row['percent']}%</span>
              <div class="small-muted">{category_name(row['category'])} • {row['score']}/{row['total']} • {row['played_at']}</div>
            </div>
            """, unsafe_allow_html=True)
    if st.button(t["back_home"]):
        go("home")

# -------------------- Admin --------------------
elif st.session_state.page == "admin":
    st.markdown("## ⚙️ " + t["admin_title"])
    st.caption(t["admin_desc"])
    with st.expander("➕ " + t["add_question"], expanded=True):
        category = st.selectbox(
            t["category"],
            list(CATEGORIES.keys()),
            format_func=lambda c: category_name(c)
        )
        q_en = st.text_area(t["question_en"], key="admin_q_en")
        q_ar = st.text_area(t["question_ar"], key="admin_q_ar")
        options_en = [st.text_input(f"{t['option_en']} {i+1}", key=f"admin_en_{i}") for i in range(4)]
        options_ar = [st.text_input(f"{t['option_ar']} {i+1}", key=f"admin_ar_{i}") for i in range(4)]
        correct = st.selectbox(t["correct"], options=list(range(4)),
                               format_func=lambda i: f"{i+1}. {options_en[i] or options_ar[i]}")
        exp_en = st.text_input(t["explanation_en"], key="admin_exp_en")
        exp_ar = st.text_input(t["explanation_ar"], key="admin_exp_ar")
        if st.button(t["save_question"], type="primary"):
            if not q_en.strip() or not q_ar.strip() or any(not x.strip() for x in options_en + options_ar):
                st.error(t["fill_fields"])
            else:
                encoded_options = [a.strip() + "||| " + b.strip()
                                   for a, b in zip(options_en, options_ar)]
                with connect() as conn:
                    conn.execute(
                        """INSERT INTO questions(category,question,options,correct_index,explanation)
                           VALUES(?,?,?,?,?)""",
                        (category, q_en.strip() + "||| " + q_ar.strip(),
                         json.dumps(encoded_options, ensure_ascii=False), correct,
                         exp_en.strip() + "||| " + exp_ar.strip())
                    )
                    conn.commit()
                st.success(t["saved"])
                st.rerun()

    st.markdown("### " + t["existing"])
    selected_category = st.selectbox(
        t["filter"], ["All categories"] + list(CATEGORIES.keys()),
        format_func=lambda c: t["all_categories"] if c == "All categories" else category_name(c)
    )
    with connect() as conn:
        if selected_category == "All categories":
            records = conn.execute("SELECT id,category,question FROM questions ORDER BY category,id").fetchall()
        else:
            records = conn.execute(
                "SELECT id,category,question FROM questions WHERE category=? ORDER BY id",
                (selected_category,)
            ).fetchall()
    for row in records:
        col1, col2 = st.columns([5, 1])
        col1.write(f"**{category_name(row['category'])}** — {localized(row['question'], lang)}")
        if col2.button(t["delete"], key=f"del_{row['id']}"):
            with connect() as conn:
                conn.execute("DELETE FROM questions WHERE id=?", (row["id"],))
                conn.commit()
            st.rerun()
    st.caption(f"{t['shown']}: {len(records)}")
