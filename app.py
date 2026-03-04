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
    ["📖 紀錄符號一覽", "📝 建立比賽 / 登記球員",
     "🏟 比賽紀錄","🖨️ 整張紀錄表","📊 球員數據庫"]
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

elif page == "🏟 比賽紀錄":

    st.header("🏟 比賽紀錄")

    if not os.path.exists(PLAYERS_FILE):
        st.warning("請先建立比賽並登記球員")
        st.stop()

    players = pd.read_csv(PLAYERS_FILE)

    # 初始化 session
    if "inning" not in st.session_state:
        st.session_state.inning = 1
        st.session_state.half = "上"
        st.session_state.score_home = 0
        st.session_state.score_away = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("⬅ 上一局"):
            if st.session_state.inning > 1:
                st.session_state.inning -= 1

    with col2:
        st.subheader(f"第 {st.session_state.inning} 局 {st.session_state.half} 半")

    with col3:
        if st.button("下一局 ➡"):
            st.session_state.inning += 1

    st.divider()

    st.subheader("比分")

    score_col1, score_col2 = st.columns(2)

    with score_col1:
        st.metric("主隊", st.session_state.score_home)

    with score_col2:
        st.metric("客隊", st.session_state.score_away)

    st.divider()

    st.subheader("選擇打者")

    batter = st.selectbox("打者", players["姓名"].unique())

    st.subheader("打席結果")

    result = st.selectbox(
        "選擇結果",
        ["安打", "全壘打", "四壞", "三振", "滾地出局", "飛球出局"]
    )

    rbi = st.number_input("打點", 0)
    run = st.number_input("得分", 0)

    if st.button("紀錄打席"):

        game_data = {
            "game_id": "game_001",
            "局數": st.session_state.inning,
            "半局": st.session_state.half,
            "打者": batter,
            "結果": result,
            "打點": rbi,
            "得分": run
        }

        if os.path.exists("games_log.csv"):
            old = pd.read_csv("games_log.csv")
            new = pd.concat([old, pd.DataFrame([game_data])])
        else:
            new = pd.DataFrame([game_data])

        new.to_csv("games_log.csv", index=False)

        # 更新比分
        if st.session_state.half == "上":
            st.session_state.score_away += run
        else:
            st.session_state.score_home += run

        st.success("已紀錄")

    st.divider()

    if st.button("🔁 攻守交換"):
        st.session_state.half = "下" if st.session_state.half == "上" else "上"

    if st.button("🏁 終場比賽"):
        st.success("比賽結束")

elif page == "📊 球員數據庫":

    st.header("📊 球員數據庫")

    if not os.path.exists("players_stats.csv"):
        st.warning("尚未有球員數據")
        st.stop()

    stats = pd.read_csv("players_stats.csv")

    # 左側選擇球員
    player_name = st.sidebar.selectbox(
        "選擇球員",
        stats["姓名"].unique()
    )

    player = stats[stats["姓名"] == player_name].iloc[0]

    AB = player["打數"]
    H = player["安打"]
    HR = player["全壘打"]
    BB = player["四壞"]

    AVG = round(H/AB,3) if AB>0 else 0
    SLG = round((H + HR*3)/AB,3) if AB>0 else 0
    OBP = round((H+BB)/(AB+BB),3) if (AB+BB)>0 else 0
    OPS = round(OBP + SLG,3)

    col1,col2,col3 = st.columns(3)

    col1.metric("打數", AB)
    col2.metric("安打", H)
    col3.metric("全壘打", HR)

    col4,col5,col6 = st.columns(3)

    col4.metric("四壞", BB)
    col5.metric("打擊率 AVG", AVG)
    col6.metric("OPS", OPS)

    st.divider()

    st.subheader("完整原始數據")

    st.dataframe(stats, use_container_width=True)

elif page == "🖨️ 整張紀錄表":

    innings = 12

    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "全表"

    if "selected_inning" not in st.session_state:
        st.session_state.selected_inning = 1

    # =========================
    # 全表模式
    # =========================
    if st.session_state.view_mode == "全表":

        st.header("🖨️ 棒球整張紀錄表")

        # ---------- 局數列 ----------
        cols = st.columns(innings + 1)

        cols[0].markdown("**棒次**")

        for i in range(innings):
            if cols[i+1].button(
                str(i+1),
                key=f"inning_btn_{i}",
                use_container_width=True
            ):
                st.session_state.selected_inning = i+1
                st.session_state.view_mode = "單局"
                st.rerun()

        # ---------- 1-9棒 ----------
        for order in range(1, 10):

            row_cols = st.columns(innings + 1)

            row_cols[0].markdown(f"**{order}**")

            for i in range(innings):
                row_cols[i+1].write("□")

        # ---------- P 行 ----------
        p_cols = st.columns(innings + 1)
        p_cols[0].markdown("**P**")

        for i in range(innings):
            p_cols[i+1].write("□")

    # =========================
    # 單局模式
    # =========================
    else:

        inning = st.session_state.selected_inning

        st.header(f"第 {inning} 局")

        if st.button("⬅ 返回整張表"):
            st.session_state.view_mode = "全表"
            st.rerun()

        st.divider()

        col1, col2 = st.columns([1,3])

        with col1:
            st.subheader("先發名單")
            for i in range(1,10):
                st.write(f"{i}  #__  姓名")

        with col2:
            st.subheader("本局打席")
            for i in range(1,10):
                st.write(f"{i}棒  □ □ □")
