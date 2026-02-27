import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide")

st.title("⚾ 台灣傳統逐球紀錄系統 V1")

# ==============================
# 初始化
# ==============================

if "game" not in st.session_state:
    st.session_state.game = []

if "current_pa" not in st.session_state:
    st.session_state.current_pa = []

# ==============================
# 基本資訊
# ==============================

col1, col2 = st.columns(2)

with col1:
    game_date = st.date_input("比賽日期", datetime.today())

with col2:
    opponent = st.text_input("對戰球隊")

st.divider()

# ==============================
# 逐球紀錄區
# ==============================

st.header("🎯 逐球紀錄")

cols = st.columns(6)

symbols = {
    "O": "看好球",
    "Ø": "揮棒好球",
    "△": "界外球",
    "—": "壞球",
    "●": "擊球進場",
}

for i, (sym, text) in enumerate(symbols.items()):
    if cols[i].button(f"{sym}\n{text}"):
        st.session_state.current_pa.append(sym)

# 清除按鈕
if st.button("清除本打席"):
    st.session_state.current_pa = []

st.subheader("目前逐球紀錄")
st.write(" ".join(st.session_state.current_pa))

# ==============================
# 自動球數判斷
# ==============================

balls = st.session_state.current_pa.count("—")
strikes = (
    st.session_state.current_pa.count("O")
    + st.session_state.current_pa.count("Ø")
    + st.session_state.current_pa.count("△")
)

st.write(f"壞球: {balls}   好球: {strikes}")

# 自動三振判斷
if strikes >= 3:
    st.warning("⚠ 三振成立")

# 自動四壞判斷
if balls >= 4:
    st.warning("⚠ 四壞成立")

# ==============================
# 打席結果
# ==============================

st.divider()
st.header("📌 打席結果")

result = st.selectbox(
    "選擇結果",
    ["", "1B", "2B", "3B", "HR", "BB", "K", "OUT", "SF"],
)

if st.button("完成打席"):

    if result == "":
        st.error("請選擇結果")
    else:
        st.session_state.game.append(
            {
                "pitches": st.session_state.current_pa.copy(),
                "result": result,
            }
        )
        st.session_state.current_pa = []
        st.success("打席已完成")

# ==============================
# 本場統計
# ==============================

st.divider()
st.header("📊 本場統計")

AB = 0
H = 0
TB = 0
BB = 0
SF = 0

for pa in st.session_state.game:

    r = pa["result"]

    if r == "1B":
        AB += 1
        H += 1
        TB += 1

    elif r == "2B":
        AB += 1
        H += 1
        TB += 2

    elif r == "3B":
        AB += 1
        H += 1
        TB += 3

    elif r == "HR":
        AB += 1
        H += 1
        TB += 4

    elif r == "BB":
        BB += 1

    elif r == "SF":
        SF += 1

    elif r in ["K", "OUT"]:
        AB += 1

# 計算數據
AVG = H / AB if AB > 0 else 0
OBP = (H + BB) / (AB + BB + SF) if (AB + BB + SF) > 0 else 0
SLG = TB / AB if AB > 0 else 0
OPS = OBP + SLG

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("打數", AB)
col2.metric("安打", H)
col3.metric("打擊率", round(AVG, 3))
col4.metric("上壘率", round(OBP, 3))
col5.metric("長打率", round(SLG, 3))
col6.metric("OPS", round(OPS, 3))

# ==============================
# 顯示所有打席
# ==============================

st.divider()
st.header("📄 打席紀錄")

for i, pa in enumerate(st.session_state.game):
    st.write(
        f"打席 {i+1}：{' '.join(pa['pitches'])} → {pa['result']}"
    )
