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
# 初始化
# ======================

if not os.path.exists(TEAM_FILE):

    pd.DataFrame(

    columns=["姓名","背號"]

    ).to_csv(TEAM_FILE,index=False)



if not os.path.exists(GAME_FILE):

    pd.DataFrame(

    columns=["比賽ID","日期","對手"]

    ).to_csv(GAME_FILE,index=False)



if not os.path.exists(LINEUP_FILE):

    pd.DataFrame(

    columns=[

    "比賽ID",

    "棒次",

    "姓名",

    "背號",

    "守位"

    ]

    ).to_csv(LINEUP_FILE,index=False)



# ======================
# 球員名單管理
# ======================

st.header("👥 球隊30人名單")


team_df=pd.read_csv(TEAM_FILE)



c1,c2=st.columns(2)


with c1:

    new_player=st.text_input("球員姓名")


with c2:

    new_number=st.number_input(

    "背號",

    0,

    999,

    0

    )



if st.button("新增球員"):

    if new_player.strip()=="":

        st.warning("請輸入姓名")

        st.stop()


    if new_number==0:

        st.warning("請輸入背號")

        st.stop()


    new=pd.DataFrame([{

    "姓名":new_player.strip(),

    "背號":int(new_number)

    }])


    team_df=pd.concat(

    [team_df,new],

    ignore_index=True

    )


    team_df.to_csv(

    TEAM_FILE,

    index=False

    )

    st.success("新增成功")

    st.rerun()



# ======================
# 顯示名單＋刪除
# ======================

st.subheader("目前名單")


if team_df.empty:

    st.info("尚未建立球員")

else:

    for i,row in team_df.iterrows():

        colA,colB=st.columns([9,1])

        with colA:

            st.write(

            f"#{int(row['背號'])}  {row['姓名']}"

            )

        with colB:

            if st.button(

            "❌",

            key=f"delplayer{i}"

            ):

                team_df=team_df.drop(i)

                team_df.to_csv(

                TEAM_FILE,

                index=False

                )

                st.success("已刪除")

                st.rerun()



# ======================
# 建立比賽
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

    st.success("建立成功")

    st.rerun()



# ======================
# 選擇比賽
# ======================

st.header("🎮 選擇比賽")


game_df=pd.read_csv(GAME_FILE)


if game_df.empty:

    st.info("尚無比賽")

    st.stop()



game_df["顯示"]=(
game_df["比賽ID"]
+" ｜ "
+game_df["日期"]
+" vs "
+game_df["對手"]
)


select=st.selectbox(

"選擇比賽",

game_df["顯示"]

)


game_id=select.split(" ｜ ")[0]



# ======================
# 先發名單
# ======================

st.header("📋 先發名單")


team_df=pd.read_csv(TEAM_FILE)


if team_df.empty:

    st.warning("請先新增球員")

    st.stop()


team_df["顯示"]=(
"#"
+team_df["背號"].astype(str)
+" "
+team_df["姓名"]
)


players=team_df["顯示"].tolist()


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

        number=batter.split(" ")[0].replace("#","")

        name=batter.split(" ")[1]


        new=pd.DataFrame([{

        "比賽ID":game_id,

        "棒次":i,

        "姓名":name,

        "背號":number,

        "守位":pos

        }])


        lineup_df=pd.concat(

        [lineup_df,new],

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

    st.info("尚未建立")

else:

    st.dataframe(

    show.sort_values("棒次"),

    use_container_width=True

    )



# ======================
# 局數紀錄
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


st.info(

f"{inning}局 ｜ {side}"

)
