import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid


st.set_page_config(layout="wide")

st.title("⚾棒球比賽紀錄系統")


TEAM_FILE="team.csv"
GAME_FILE="games.csv"
LINEUP_FILE="lineup.csv"


# ======================
# 初始化CSV
# ======================

if not os.path.exists(TEAM_FILE):

    pd.DataFrame(columns=["姓名"]).to_csv(TEAM_FILE,index=False)


if not os.path.exists(GAME_FILE):

    pd.DataFrame(

    columns=["比賽ID","日期","對手"]

    ).to_csv(GAME_FILE,index=False)


if not os.path.exists(LINEUP_FILE):

    pd.DataFrame(

    columns=["比賽ID","棒次","姓名","守位"]

    ).to_csv(LINEUP_FILE,index=False)



# ======================
# 名單管理
# ======================

st.header("👥 球隊30人名單")

team_df=pd.read_csv(TEAM_FILE)

new_player=st.text_input("新增球員")


if st.button("新增球員"):

    if new_player.strip()!="":

        team_df=pd.concat(

        [

        team_df,

        pd.DataFrame([{

        "姓名":new_player.strip()

        }])

        ],

        ignore_index=True

        )

        team_df.to_csv(

        TEAM_FILE,

        index=False

        )

        st.rerun()



st.dataframe(team_df,use_container_width=True)



# ======================
# 建立比賽（穩定版）
# ======================

st.header("📅 建立比賽")


date=st.date_input(

"比賽日期",

datetime.today()

)

opponent=st.text_input("對手")


if st.button("建立新比賽"):

    if opponent.strip()=="":

        st.warning("請輸入對手")

        st.stop()


    game_df=pd.read_csv(GAME_FILE)


    gid=str(uuid.uuid4())


    new=pd.DataFrame([{

    "比賽ID":gid,

    "日期":date.strftime("%Y-%m-%d"),

    "對手":opponent

    }])


    game_df=pd.concat(

    [game_df,new],

    ignore_index=True

    )


    game_df.to_csv(

    GAME_FILE,

    index=False

    )


    st.success("✅ 建立成功")

    st.rerun()



# ======================
# 選擇比賽
# ======================

st.header("🎮 選擇比賽")

game_df=pd.read_csv(GAME_FILE)

game_df=game_df.fillna("")


if game_df.empty:

    st.info("尚無比賽")

    st.stop()


game_df["顯示"]=(

game_df["比賽ID"].astype(str)

+" ｜ "

+game_df["日期"].astype(str)

+" vs "

+game_df["對手"].astype(str)

)


game_select=st.selectbox(

"選擇比賽",

game_df["顯示"].tolist()

)


game_id=game_select.split(" ｜ ")[0]



# ======================
# 先發名單
# ======================

st.header("📋 先發名單")


team_df=pd.read_csv(TEAM_FILE)


if team_df.empty:

    st.warning("請先新增球員")

    st.stop()


players=team_df["姓名"].tolist()


positions=[

"CF","RF","LF",

"1B","2B","3B",

"SS","C","DH","P"

]


lineup_df=pd.read_csv(LINEUP_FILE)


for i in range(1,10):

    c1,c2=st.columns(2)


    with c1:

        batter=st.selectbox(

        f"{i}棒",

        players,

        key=f"bat{i}"

        )


    with c2:

        pos=st.selectbox(

        "守位",

        positions,

        key=f"pos{i}"

        )


    if st.button(

    f"登記{i}棒",

    key=f"save{i}"

    ):

        new=pd.DataFrame([{

        "比賽ID":game_id,

        "棒次":i,

        "姓名":batter,

        "守位":pos

        }])


        lineup_df=pd.concat(

        [

        lineup_df,

        new

        ],

        ignore_index=True

        )


        lineup_df.to_csv(

        LINEUP_FILE,

        index=False

        )

        st.success("已登記")

        st.rerun()



# ======================
# 顯示先發
# ======================

st.header("⭐本場先發")


show=lineup_df[

lineup_df["比賽ID"]

==game_id

]


if show.empty:

    st.info("尚未建立先發")

else:

    st.dataframe(

    show.sort_values("棒次"),

    use_container_width=True

    )



# ======================
# 局數紀錄（示範）
# ======================

st.header("📝 局數紀錄")


inning=st.number_input(

"局數",

1,

12,

1

)


side=st.radio(

"攻守",

["我方進攻","對手進攻"]

)


st.write(

f"目前紀錄：{inning}局 {side}"

)


st.info(

"下一步會升級成真正紀錄表"

)
