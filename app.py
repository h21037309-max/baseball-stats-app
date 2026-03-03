import streamlit as st
import pandas as pd
import uuid
import os

PLAYERS_FILE = "players_master.csv"

st.set_page_config(layout="wide")

st.title("⚾ 棒球紀錄系統")

# ===============================
# 側邊頁面選單
# ===============================

page = st.sidebar.radio(
    "功能選單",
    ["📖 紀錄符號一覽", "📝 建立比賽 / 登記球員"]
)

# =========================================================
# 📖 第一頁：完整中華職棒紀錄符號
# =========================================================

if page == "📖 紀錄符號一覽":

    st.title("📖 中華職棒紀錄符號一覽")

    # ① 守備位置
    st.header("① 守備位置符號")
    st.table(pd.DataFrame({
        "符號":[1,2,3,4,5,6,7,8,9,"1–9"],
        "說明":[
            "投手","捕手","一壘手","二壘手","三壘手",
            "游擊手","左外野","中外野","右外野","擊球員棒次"
        ]
    }))

    # ② 球數
    st.header("② 球數欄內使用之符號")
    st.table(pd.DataFrame({
        "符號":["○","⊖","－","◎","△","△(上)","△(左)","△(右)","▲","—","•",">"],
        "說明":[
            "好球(未揮棒)","揮棒落空","壞球","揮擊漏空",
            "界外球","後方界外","左界外","右界外",
            "擦棒被捕","觸擊球","方向點","兩好球再觸擊"
        ]
    }))

    # ③ 中央菱形
    st.header("③ 中央菱形格子內之符號")
    st.table(pd.DataFrame({
        "符號":["I","II","III","○","◎","ℓ"],
        "說明":["第一出局","第二出局","第三出局","投手失分","投手自責分","殘壘"]
    }))

    # ④ 擊出球性質
    st.header("④ 擊出球性質符號")
    st.table(pd.DataFrame({
        "符號":["︶","︿","－"],
        "說明":["滾地球","高飛球","平飛球"]
    }))

    # ⑤ 上壘
    st.header("⑤ 擊球員上壘之符號")
    st.table(pd.DataFrame({
        "符號":["／","＞","∧","◇","◇◇","B","B′","D","SFC4","K＋WP","E9"],
        "說明":[
            "一壘安打","二壘安打","三壘安打","全壘打",
            "場內全壘打","四壞球","故意四壞","觸身球",
            "野手選擇","不死三振上壘","失誤"
        ]
    }))

    # ⑥ 擊球員出局
    st.header("⑥ 擊球員出局之符號")
    st.table(pd.DataFrame({
        "符號":["K","K¹","K₂","5-3","3A","5T","F7","IF","SF"],
        "說明":[
            "三振","第三好球捕逸","捕手刺殺",
            "滾地刺殺","自行踩壘","觸殺",
            "飛球接殺","內野高飛","犧牲飛球"
        ]
    }))

    # ⑦ 跑壘進壘
    st.header("⑦ 跑壘員進壘之符號")
    st.table(pd.DataFrame({
        "符號":["S","DS","TS","WP","BK","PB","①","OB"],
        "說明":["盜壘","雙盜壘","三盜壘","暴投","投手犯規","捕逸","有打點","妨礙跑壘"]
    }))

    # ⑧ 跑壘出局
    st.header("⑧ 跑壘員出局之符號")
    st.table(pd.DataFrame({
        "符號":["6–4","5T","DP","TP"],
        "說明":["封殺","觸殺","雙殺","三殺"]
    }))

    # ⑨ 其他（更換投手反向符號）
    st.header("⑨ 其他")
    st.table(pd.DataFrame({
        "符號":["┌","｜","PH","PR","DH","／／","／／／"],
        "說明":[
            "更換投手",
            "更換打者",
            "代打",
            "代跑",
            "指定打擊",
            "半局結束",
            "比賽提前結束"
        ]
    }))

# =========================================================
# 📝 第二頁：建立比賽
# =========================================================

elif page == "📝 建立比賽 / 登記球員":

    st.header("📝 建立比賽")

    col1, col2 = st.columns(2)

    with col1:
        home_team = st.text_input("主隊名稱")

    with col2:
        away_team = st.text_input("客隊名稱")

    st.subheader("主隊球員名單")
    home_players = st.data_editor(
        pd.DataFrame(columns=["背號", "姓名"]),
        num_rows="dynamic",
        key="home_editor"
    )

    st.subheader("客隊球員名單")
    away_players = st.data_editor(
        pd.DataFrame(columns=["背號", "姓名"]),
        num_rows="dynamic",
        key="away_editor"
    )

    if st.button("✅ 建立比賽並儲存球員"):

        all_players = []

        for _, row in home_players.iterrows():
            if pd.notna(row["姓名"]):
                all_players.append({
                    "player_id": str(uuid.uuid4()),
                    "球隊": home_team,
                    "背號": row["背號"],
                    "姓名": row["姓名"]
                })

        for _, row in away_players.iterrows():
            if pd.notna(row["姓名"]):
                all_players.append({
                    "player_id": str(uuid.uuid4()),
                    "球隊": away_team,
                    "背號": row["背號"],
                    "姓名": row["姓名"]
                })

        new_df = pd.DataFrame(all_players)

        if os.path.exists(PLAYERS_FILE):
            old_df = pd.read_csv(PLAYERS_FILE)
            final_df = pd.concat([old_df, new_df], ignore_index=True)
        else:
            final_df = new_df

        final_df.to_csv(PLAYERS_FILE, index=False)

        st.success("比賽建立完成，球員已加入後台資料庫")
        st.balloons()
