import streamlit as st
import pandas as pd
import os
import uuid

st.set_page_config(layout="wide")
st.title("⚾ 校隊棒球管理系統 V2")

# ======================
# 檔案設定
# ======================

USER_FILE = "users.csv"
PLAYER_FILE = "players.csv"

# ======================
# 初始化 users
# ======================

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=[
        "user_id","帳號","密碼","球隊名稱"
    ]).to_csv(USER_FILE,index=False)

if not os.path.exists(PLAYER_FILE):
    pd.DataFrame(columns=[
        "player_id","user_id","姓名","背號","守位","投打"
    ]).to_csv(PLAYER_FILE,index=False)

users = pd.read_csv(USER_FILE)
players = pd.read_csv(PLAYER_FILE)

# ======================
# 登入 / 註冊
# ======================

mode = st.sidebar.radio("帳號",["登入","註冊"])

# ===== 註冊 =====

if mode == "註冊":

    st.header("建立教練帳號")

    acc = st.text_input("帳號")
    pw = st.text_input("密碼",type="password")
    team = st.text_input("球隊名稱")

    if st.button("建立帳號"):

        if acc in users["帳號"].astype(str).values:
            st.error("帳號已存在")
        else:
            new_user = pd.DataFrame([{
                "user_id": str(uuid.uuid4()),
                "帳號": acc,
                "密碼": pw,
                "球隊名稱": team
            }])

            users = pd.concat([users,new_user],ignore_index=True)
            users.to_csv(USER_FILE,index=False)
            st.success("註冊成功")

    st.stop()

# ===== 登入 =====

username = st.sidebar.text_input("帳號")
password = st.sidebar.text_input("密碼",type="password")

login = users[
(users["帳號"]==username)&
(users["密碼"]==password)
]

if login.empty:
    st.warning("請登入")
    st.stop()

user_id = login.iloc[0]["user_id"]
team_name = login.iloc[0]["球隊名稱"]

st.success(f"目前球隊：{team_name}")

st.divider()

# ======================
# 球員管理
# ======================

st.header("👥 球員管理")

team_players = players[players["user_id"]==user_id]

# ===== 新增球員 =====

with st.form("add_player"):

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        name = st.text_input("姓名")

    with col2:
        number = st.number_input("背號",0)

    with col3:
        position = st.text_input("守位")

    with col4:
        hand = st.selectbox("投打",["右投右打","右投左打","左投左打","左投右打"])

    submit = st.form_submit_button("新增球員")

    if submit:

        if name == "":
            st.warning("請輸入姓名")
        elif len(team_players) >= 30:
            st.error("已達30人上限")
        else:
            new_player = pd.DataFrame([{
                "player_id": str(uuid.uuid4()),
                "user_id": user_id,
                "姓名": name,
                "背號": number,
                "守位": position,
                "投打": hand
            }])

            players = pd.concat([players,new_player],ignore_index=True)
            players.to_csv(PLAYER_FILE,index=False)
            st.success("新增完成")
            st.rerun()

st.divider()

# ===== 顯示球員 =====

st.subheader("目前球員名單")

if team_players.empty:
    st.info("尚未新增球員")
else:

    for _,row in team_players.iterrows():

        colA,colB,colC,colD,colE = st.columns([2,1,2,2,1])

        colA.write(row["姓名"])
        colB.write(f"#{int(row['背號'])}")
        colC.write(row["守位"])
        colD.write(row["投打"])

        if colE.button("刪除",key=row["player_id"]):

            players = players[
            players["player_id"]!=row["player_id"]
            ]

            players.to_csv(PLAYER_FILE,index=False)
            st.success("已刪除")
            st.rerun()
