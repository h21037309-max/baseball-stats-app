import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

st.set_page_config(layout="wide")

st.title("⚾棒球紀錄系統")

TEAM="team.csv"
GAME="games.csv"
LINEUP="lineup.csv"


# =====================
# 初始化
# =====================

def init(path,cols):
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_csv(path,index=False)

init(TEAM,["player_id","姓名","背號"])
init(GAME,["比賽ID","日期","對手"])
init(LINEUP,["比賽ID","棒次","player_id","守位"])


team=pd.read_csv(TEAM)
games=pd.read_csv(GAME)
lineup=pd.read_csv(LINEUP)


# =====================
# 球員
# =====================

st.header("👥 球員")

c1,c2=st.columns(2)

name=c1.text_input("姓名")
num=c2.number_input("背號",1,999)

if st.button("新增球員"):

    if name.strip()=="":
        st.warning("姓名空白")

    else:

        new=pd.DataFrame([{

        "player_id":str(uuid.uuid4()),
        "姓名":name.strip(),
        "背號":int(num)

        }])

        team=pd.concat([team,new],ignore_index=True)

        team.to_csv(TEAM,index=False)

        st.rerun()


st.subheader("名單")

for _,r in team.reset_index().iterrows():

    a,b=st.columns([9,1])

    a.write(f"#{r['背號']} {r['姓名']}")

    if b.button("刪除",key=r["player_id"]):

        team=team[team["player_id"]!=r["player_id"]]

        team.to_csv(TEAM,index=False)

        st.rerun()


# =====================
# 建立比賽
# =====================

st.header("📅 建立比賽")

date=st.date_input("日期",datetime.today())

opp=st.text_input("對手")

if st.button("建立"):

    if opp.strip()=="":
        st.warning("輸入對手")

    else:

        new=pd.DataFrame([{

        "比賽ID":str(uuid.uuid4()),
        "日期":date.strftime("%Y-%m-%d"),
        "對手":opp

        }])

        games=pd.concat([games,new],ignore_index=True)

        games.to_csv(GAME,index=False)

        st.success("建立成功")

        st.rerun()



# =====================
# 選擇比賽
# =====================

st.header("🎮 比賽")

if games.empty:

    st.info("尚未建立")

    st.stop()


games["顯示"]=games["日期"]+" vs "+games["對手"]

selected=st.selectbox(

"選擇比賽",

games["顯示"].tolist()

)

game_id=games.loc[
games["顯示"]==selected,
"比賽ID"
].values[0]


# =====================
# 先發
# =====================

st.header("📋先發")

if team.empty:

    st.warning("沒有球員")

    st.stop()


team["顯示"]="#"+team["背號"].astype(str)+" "+team["姓名"]

positions=["CF","RF","LF","1B","2B","3B","SS","C","DH","P"]

for i in range(1,10):

    c1,c2=st.columns(2)

    batter=c1.selectbox(

    f"{i}棒",

    team["顯示"],

    key=f"bat{i}"

    )

    pos=c2.selectbox(

    "守位",

    positions,

    key=f"pos{i}"

    )

    if st.button("儲存",key=f"save{i}"):

        pid=team.loc[
        team["顯示"]==batter,
        "player_id"
        ].values[0]

        lineup=lineup[
        ~(
        (lineup["比賽ID"]==game_id)&
        (lineup["棒次"]==i)
        )
        ]

        new=pd.DataFrame([{

        "比賽ID":game_id,
        "棒次":i,
        "player_id":pid,
        "守位":pos

        }])

        lineup=pd.concat([lineup,new],ignore_index=True)

        lineup.to_csv(LINEUP,index=False)

        st.success("完成")

        st.rerun()


# =====================
# 顯示先發
# =====================

st.header("⭐本場先發")

current=lineup[lineup["比賽ID"]==game_id]

if current.empty:

    st.info("未設定")

else:

    show=current.merge(team,on="player_id")

    st.dataframe(

    show[["棒次","背號","姓名","守位"]]
    .sort_values("棒次"),

    use_container_width=True

    )


# =====================
# 局數
# =====================

st.header("📝局數")

inning=st.number_input("局",1,12,1)

side=st.radio("攻守",["我方","對手"])

st.success(f"{inning}局 {side}")
