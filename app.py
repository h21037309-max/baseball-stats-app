import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

st.set_page_config(layout="wide")

st.title("⚾ 12局雙隊逐球紀錄系統 V1")

# ======================
# 檔案
# ======================

TEAM_FILE = "team.csv"
PA_FILE = "plate_appearances.csv"

# 初始化檔案
if not os.path.exists(TEAM_FILE):
    pd.DataFrame(columns=["player_id","姓名","背號"]).to_csv(TEAM_FILE,index=False)

if not os.path.exists(PA_FILE):
    pd.DataFrame(columns=[
        "game_id","inning","half","team",
        "batter","pitch_seq","result"
    ]).to_csv(PA_FILE,index=False)

team_df = pd.read_csv(TEAM_FILE)
pa_df = pd.read_csv(PA_FILE)

# ======================
# Session 初始化
# ======================

if "game_id" not in st.session_state:
    st.session_state.game_id = str(uuid.uuid4())
    st.session_state.inning = 1
    st.session_state.half = "top"  # top=對手攻, bot=我方攻
    st.session_state.outs = 0
    st.session_state.pitch_seq = ""
    st.session_state.lineup_home = []
    st.session_state.lineup_away = []
    st.session_state.current_index = 0

# ======================
# 先發設定
# ======================

st.header("⚾ 先發設定")

col1, col2 = st.columns(2)

with col1:
    st.subheader("我方 1~9棒")
    home_lineup = []
    for i in range(9):
        player = st.selectbox(
            f"{i+1}棒",
            team_df["姓名"].tolist(),
            key=f"home_{i}"
        )
        home_lineup.append(player)

with col2:
    st.subheader("對手 1~9 背號")
    away_lineup = []
    for i in range(9):
        num = st.number_input(
            f"{i+1}棒背號",
            0,999,0,
            key=f"away_{i}"
        )
        away_lineup.append(f"#{num}")

if st.button("開始比賽"):
    st.session_state.lineup_home = home_lineup
    st.session_state.lineup_away = away_lineup
    st.success("比賽開始！")
    st.rerun()

# ======================
# 比賽畫面
# ======================

if st.session_state.lineup_home:

    st.divider()

    if st.session_state.inning > 12:
        st.success("🎉 比賽結束（12局）")
        st.stop()

    half_text = "上半局（對手攻）" if st.session_state.half=="top" else "下半局（我方攻）"

    st.header(f"第 {st.session_state.inning} 局 {half_text}")
    st.write(f"出局數：{st.session_state.outs}")

    # 目前打者
    if st.session_state.half == "top":
        lineup = st.session_state.lineup_away
    else:
        lineup = st.session_state.lineup_home

    batter = lineup[st.session_state.current_index % 9]
    st.subheader(f"目前打者：{batter}")

    st.write(f"逐球紀錄：{st.session_state.pitch_seq}")

    # ======================
    # 逐球按鈕
    # ======================

    colA, colB, colC, colD = st.columns(4)

    if colA.button("— 壞球"):
        st.session_state.pitch_seq += "— "
        st.rerun()

    if colB.button("O 好球"):
        st.session_state.pitch_seq += "O "
        st.rerun()

    if colC.button("Ø 揮空"):
        st.session_state.pitch_seq += "Ø "
        st.rerun()

    if colD.button("△ 界外"):
        st.session_state.pitch_seq += "△ "
        st.rerun()

    st.divider()
    st.subheader("打席結果")

    result_cols = st.columns(4)

    results = ["H","2B","3B","HR","BB","K","GO","FO"]

    for i,res in enumerate(results):
        if result_cols[i%4].button(res, key=f"res_{res}"):

            # 存檔
            new_row = pd.DataFrame([{
                "game_id":st.session_state.game_id,
                "inning":st.session_state.inning,
                "half":st.session_state.half,
                "team":"away" if st.session_state.half=="top" else "home",
                "batter":batter,
                "pitch_seq":st.session_state.pitch_seq,
                "result":res
            }])

            pa_df = pd.concat([pa_df,new_row],ignore_index=True)
            pa_df.to_csv(PA_FILE,index=False)

            # 出局計算
            if res in ["K","GO","FO"]:
                st.session_state.outs += 1

            # 換下一棒
            st.session_state.current_index += 1
            st.session_state.pitch_seq = ""

            # 三出局換半局
            if st.session_state.outs >= 3:
                st.session_state.outs = 0
                st.session_state.current_index = 0

                if st.session_state.half == "top":
                    st.session_state.half = "bot"
                else:
                    st.session_state.half = "top"
                    st.session_state.inning += 1

            st.rerun()
