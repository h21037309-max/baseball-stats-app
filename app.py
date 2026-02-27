import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

st.set_page_config(layout="wide")
st.title("⚾棒球紀錄系統（穩定版）")

TEAM_FILE="team.csv"
GAME_FILE="games.csv"
LINEUP_FILE="lineup.csv"

# ======================
# 初始化
# ======================

def init_file(path,columns):
    if not os.path.exists(path):
        pd.DataFrame(columns=columns).to_csv(path,index=False)

init_file(TEAM_FILE,["player_id","姓名","背號"])
init_file(GAME_FILE,["比賽ID","日期","對手"])
init_file(LINEUP_FILE,["比賽ID","棒次","player_id","守位"])

team_df=pd.read_csv(TEAM_FILE)
game_df=pd.read_csv(GAME_FILE)
lineup_df=pd.read_csv(LINEUP_FILE)

# ======================
# 球員管理
# ======================

st.header("👥 球員名單")

col1,col2=st.columns(2)

with col1:
    new_name=st.text_input("姓名")

with col2:
    new_number=st.number_input("背號",1,999)

if st.button("新增球員"):
    if new_name.strip()=="":
        st.warning("請輸入姓名")
    else:
        new=pd.DataFrame([{
            "player_id":str(uuid.uuid4()),
            "姓名":new_name.strip(),
            "背號":int(new_number)
        }])
        team_df=pd.concat([team_df,new],ignore_index=True)
        team_df.to_csv(TEAM_FILE,index=False)
        st.rerun()

st.subheader("目前名單")

if team_df.empty:
    st.info("尚無球員")
else:
    for idx,row in team_df.iterrows():
        colA,colB=st.columns([9,1])
        colA.write(f"#{row['背號']} {row['姓名']}")
        if colB.button("❌",key=row["player_id"]):
            team_df=team_df[team_df["player_id"]!=row["player_id"]]
            team_df.to_csv(TEAM_FILE,index=False)
            st.rerun()

# ======================
# 建立比賽
# ======================

st.header("📅 建立比賽")

date=st.date_input("日期",datetime.today())
opponent=st.text_input("對手")

if st.button("建立比賽"):
    if opponent.strip()=="":
        st.warning("請輸入對手")
    else:
        new=pd.DataFrame([{
            "比賽ID":str(uuid.uuid4()),
            "日期":date.strftime("%Y-%m-%d"),
            "對手":opponent.strip()
        }])
        game_df=pd.concat([game_df,new],ignore_index=True)
        game_df.to_csv(GAME_FILE,index=False)
        st.rerun()

# ======================
# 選擇比賽
# ======================

st.header("🎮 選擇比賽")

if game_df.empty:
    st.info("尚無比賽")
    st.stop()

game_df["顯示"]=(
    game_df["日期"]+" vs "+game_df["對手"]
)

selected=st.selectbox("選擇",game_df["顯示"])
game_id=game_df.iloc[game_df["顯示"]==selected].iloc[0]["比賽ID"]

# ======================
# 先發名單
# ======================

st.header("📋 先發名單")

if team_df.empty:
    st.warning("請先建立球員")
    st.stop()

team_df["顯示"]=(
    "#"+team_df["背號"].astype(str)+" "+team_df["姓名"]
)

positions=["CF","RF","LF","1B","2B","3B","SS","C","DH","P"]

for i in range(1,10):
    col1,col2=st.columns(2)
    with col1:
        batter_display=st.selectbox(f"{i}棒",team_df["顯示"],key=f"bat{i}")
    with col2:
        pos=st.selectbox("守位",positions,key=f"pos{i}")

    if st.button(f"儲存{i}棒",key=f"save{i}"):

        player_id=team_df.iloc[
            team_df["顯示"]==batter_display
        ].iloc[0]["player_id"]

        lineup_df=lineup_df[
            ~(
                (lineup_df["比賽ID"]==game_id)&
                (lineup_df["棒次"]==i)
            )
        ]

        new=pd.DataFrame([{
            "比賽ID":game_id,
            "棒次":i,
            "player_id":player_id,
            "守位":pos
        }])

        lineup_df=pd.concat([lineup_df,new],ignore_index=True)
        lineup_df.to_csv(LINEUP_FILE,index=False)
        st.rerun()

# ======================
# 顯示先發
# ======================

st.header("⭐本場先發")

current=lineup_df[lineup_df["比賽ID"]==game_id]

if current.empty:
    st.info("尚未設定")
else:
    merged=current.merge(team_df,on="player_id")
    st.dataframe(
        merged[["棒次","背號","姓名","守位"]]
        .sort_values("棒次"),
        use_container_width=True
    )

# ======================
# 局數顯示
# ======================

st.header("📝 局數紀錄（下一步會升級）")

inning=st.number_input("局數",1,12,1)
side=st.radio("攻守",["我方進攻","對手進攻"])

st.info(f"{inning}局 - {side}")
