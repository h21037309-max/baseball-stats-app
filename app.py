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
# ======================
# 逐球紀錄資料檔
# ======================

PITCH_FILE = "pitch_log.csv"

if os.path.exists(LINEUP_FILE):
    lineup_df = pd.read_csv(LINEUP_FILE)
else:
    st.error("找不到先發名單")
    st.stop()

if os.path.exists(PITCH_FILE):
    pitch_df = pd.read_csv(PITCH_FILE)
else:
    pitch_df = pd.DataFrame(columns=[
        "game_id","inning","half",
        "棒次","姓名",
        "pitch_sequence",
        "result"
    ])

# ======================
# 打席格子顯示
# ======================

st.subheader("📒 棒球紀錄表")

current_inning = game["inning"]
current_half = game["half"]

for _, player in lineup_df.iterrows():

    batter_order = player["棒次"]
    batter_name = player["姓名"]

    col1, col2 = st.columns([2,8])

    with col1:
        st.markdown(f"**{batter_order}棒 {batter_name}**")

    with col2:

        # 找出該球員本局打席數
        batter_records = pitch_df[
            (pitch_df["inning"]==current_inning) &
            (pitch_df["half"]==current_half) &
            (pitch_df["棒次"]==batter_order)
        ]

        at_bat_count = len(batter_records)

        cols = st.columns(5)

        for i in range(5):

            if i < at_bat_count:
                result = batter_records.iloc[i]["result"]
                color = "red" if result in ["1B","2B","3B","HR","BB"] else "black"
                cols[i].markdown(
                    f"<div style='text-align:center;color:{color};font-weight:bold;'>"
                    f"{result}</div>",
                    unsafe_allow_html=True
                )
            else:
                if cols[i].button("＋", key=f"new_{batter_order}_{i}"):

                    st.session_state.edit_batter = batter_order
                    st.session_state.edit_name = batter_name
                    st.session_state.pitch_sequence = []
                    st.session_state.edit_mode = True
                    st.rerun()

# ======================
# 逐球紀錄畫面
# ======================

if "edit_mode" in st.session_state and st.session_state.edit_mode:

    st.divider()
    st.header(f"🎯 逐球紀錄 - {st.session_state.edit_name}")

    pitch_seq = st.session_state.pitch_sequence

    colA, colB, colC, colD = st.columns(4)

    if colA.button("O"):
        pitch_seq.append("O")
    if colB.button("Ø"):
        pitch_seq.append("Ø")
    if colC.button("△"):
        pitch_seq.append("△")
    if colD.button("—"):
        pitch_seq.append("—")

    st.write("目前球序：", " ".join(pitch_seq))

    st.subheader("打席結果")

    result = st.selectbox(
        "選擇結果",
        ["OUT","1B","2B","3B","HR","BB"]
    )

    if st.button("💾 儲存打席"):

        new_row = pd.DataFrame([{
            "game_id": game["game_id"],
            "inning": current_inning,
            "half": current_half,
            "棒次": st.session_state.edit_batter,
            "姓名": st.session_state.edit_name,
            "pitch_sequence": " ".join(pitch_seq),
            "result": result
        }])

        pitch_df = pd.concat([pitch_df,new_row],ignore_index=True)
        pitch_df.to_csv(PITCH_FILE,index=False)

        st.session_state.edit_mode = False
        st.rerun()

    if st.button("❌ 取消"):
        st.session_state.edit_mode = False
        st.rerun()

# ======================
# Part3 自動統計同步
# ======================

st.divider()
st.header("⚙️ 自動同步逐球紀錄 → 打擊數據")

if os.path.exists("pitch_log.csv"):

    pitch_df = pd.read_csv("pitch_log.csv")

else:

    pitch_df = pd.DataFrame()


if not pitch_df.empty:

    if st.button("🔄 同步全部逐球紀錄"):

        new_rows=[]

        for _,row in pitch_df.iterrows():

            result=row["result"]

            name=row["姓名"]

            # 初始化
            AB=0
            H=0

            single=0
            double=0
            triple=0
            HR=0

            BB=0
            SF=0

            PA=1

            # ===== 打席結果判斷 =====

            if result=="OUT":

                AB=1

            elif result=="1B":

                AB=1
                H=1
                single=1

            elif result=="2B":

                AB=1
                H=1
                double=1

            elif result=="3B":

                AB=1
                H=1
                triple=1

            elif result=="HR":

                AB=1
                H=1
                HR=1

            elif result=="BB":

                BB=1

            elif result=="SF":

                SF=1

            # ===== 建立資料 =====

            new_rows.append({

            "紀錄ID":str(uuid.uuid4()),

            "日期":datetime.now().strftime("%Y-%m-%d"),

            "球隊":"AUTO",

            "背號":0,

            "姓名":name,

            "對戰球隊":"逐球紀錄",

            "打席":PA,

            "打數":AB,

            "得分":0,

            "打點":0,

            "安打":H,

            "1B":single,

            "2B":double,

            "3B":triple,

            "HR":HR,

            "BB":BB,

            "SF":SF,

            "SH":0,

            "SB":0

            })


        auto_df=pd.DataFrame(new_rows)

        df=pd.concat([df,auto_df],ignore_index=True)

        df.to_csv(DATA_FILE,index=False)

        st.success("✅ 已同步逐球紀錄")

        st.rerun()

else:

    st.info("尚無逐球紀錄")

# ======================
# 職棒逐球紀錄表
# ======================

if page=="逐球記錄表":

    st.title("⚾ 職棒逐球記錄")

    LINEUP_FILE="lineup.csv"
    PITCH_FILE="pitch_log.csv"


    # =========先發名單=========

    st.subheader("⭐先發打線")

    if os.path.exists(LINEUP_FILE):

        lineup=pd.read_csv(LINEUP_FILE)

    else:

        lineup=pd.DataFrame(columns=["棒次","姓名"])


    with st.form("lineup"):

        players=[]

        for i in range(1,10):

            name=st.text_input(f"{i}棒")

            players.append(name)

        if st.form_submit_button("儲存先發"):

            new=pd.DataFrame({

            "棒次":range(1,10),

            "姓名":players

            })

            new.to_csv(LINEUP_FILE,index=False)

            st.success("完成")

            st.rerun()


    if os.path.exists(LINEUP_FILE):

        lineup=pd.read_csv(LINEUP_FILE)

    else:

        st.stop()


    # =========局數=========

    inning=st.slider(

    "局數",

    1,9,1

    )


    offense=st.radio(

    "攻守",

    ["我方攻擊","對手攻擊"]

    )


    # =========逐球=========

    st.subheader(f"第{inning}局 {offense}")


    batter=st.selectbox(

    "打者",

    lineup["姓名"]

    )


    symbol=st.selectbox(

    "球種符號",

    [

    "O 好球",

    "揮空",

    "△界外",

    "—壞球"

    ]

    )


    result=st.selectbox(

    "結果",

    [

    "未結束",

    "OUT",

    "1B",

    "2B",

    "3B",

    "HR",

    "BB",

    "SF"

    ]

    )


    if st.button("紀錄一球"):

        new=pd.DataFrame([{

        "時間":datetime.now(),

        "局":inning,

        "攻守":offense,

        "姓名":batter,

        "符號":symbol,

        "result":result

        }])


        if os.path.exists(PITCH_FILE):

            old=pd.read_csv(PITCH_FILE)

            new=pd.concat([old,new])


        new.to_csv(PITCH_FILE,index=False)

        st.success("已紀錄")

        st.rerun()



    # =========紀錄顯示=========

    if os.path.exists(PITCH_FILE):

        log=pd.read_csv(PITCH_FILE)

        show=log[

        (log["局"]==inning)&

        (log["攻守"]==offense)

        ]


        st.dataframe(

        show.sort_values("時間",ascending=False),

        use_container_width=True
        )
