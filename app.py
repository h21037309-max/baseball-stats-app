import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

st.set_page_config(layout="wide")
st.title("⚾ 棒球專業逐球紀錄系統")

# ======================
# 檔案設定
# ======================

GAME_FILE = "current_game.json"
LINEUP_FILE = "lineup.csv"

# ======================
# 初始化比賽狀態
# ======================

def init_game():
    return {
        "game_id": str(uuid.uuid4()),
        "date": datetime.today().strftime("%Y-%m-%d"),
        "inning": 1,
        "half": "上半",   # 上半 / 下半
        "home_team": "",
        "away_team": "",
        "started": False
    }

if "game" not in st.session_state:
    st.session_state.game = init_game()

game = st.session_state.game

# ======================
# 建立新比賽
# ======================

if not game["started"]:

    st.header("📋 建立新比賽")

    col1, col2 = st.columns(2)

    with col1:
        game["home_team"] = st.text_input("我方球隊")
    with col2:
        game["away_team"] = st.text_input("對手球隊")

    st.subheader("🧢 先發名單（1~9棒）")

    lineup_data = []

    for i in range(1, 10):
        colA, colB = st.columns(2)
        with colA:
            name = st.text_input(f"{i}棒 姓名", key=f"name_{i}")
        with colB:
            position = st.text_input(f"{i}棒 守位", key=f"pos_{i}")
        lineup_data.append({
            "棒次": i,
            "姓名": name,
            "守位": position
        })

    if st.button("🚀 開始比賽"):
        df = pd.DataFrame(lineup_data)
        df.to_csv(LINEUP_FILE, index=False)
        game["started"] = True
        st.session_state.game = game
        st.rerun()

    st.stop()

# ======================
# 比賽主畫面
# ======================

st.header(f"⚾ {game['home_team']} vs {game['away_team']}")

col1, col2, col3 = st.columns([2,2,2])

with col1:
    if st.button("⬅ 上一局"):
        if game["inning"] > 1:
            game["inning"] -= 1

with col2:
    st.markdown(f"## 第 {game['inning']} 局 {game['half']}")

with col3:
    if st.button("下一局 ➡"):
        if game["inning"] < 9:
            game["inning"] += 1

col4, col5 = st.columns(2)

with col4:
    if st.button("🔁 攻守交換"):
        game["half"] = "下半" if game["half"] == "上半" else "上半"

with col5:
    if st.button("🆕 重新開始比賽"):
        st.session_state.game = init_game()
        if os.path.exists(LINEUP_FILE):
            os.remove(LINEUP_FILE)
        st.rerun()

st.session_state.game = game

st.divider()

st.info("✅ Part 1 完成：局數控制 + 攻守切換 + 先發名單建立完成")

st.write("👉 下一步 Part 2 將建立：真正棒球格子紀錄表")
