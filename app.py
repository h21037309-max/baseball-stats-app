import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(layout="wide")

st.title("⚾ 棒球專業紀錄表 V3")

GAME_FILE="games.csv"
LINEUP_FILE="lineup.csv"
PITCH_FILE="pitch_log.csv"


# ======================
# 建立CSV
# ======================

def init_csv():

    if not os.path.exists(GAME_FILE):

        pd.DataFrame(columns=[

        "比賽ID",
        "日期",
        "對手"

        ]).to_csv(GAME_FILE,index=False)


    if not os.path.exists(LINEUP_FILE):

        pd.DataFrame(columns=[

        "比賽ID",
        "棒次",
        "姓名",
        "守位"

        ]).to_csv(LINEUP_FILE,index=False)


    if not os.path.exists(PITCH_FILE):

        pd.DataFrame(columns=[

        "比賽ID",
        "局",
        "上下",
        "棒次",
        "球數"

        ]).to_csv(PITCH_FILE,index=False)

init_csv()


game_df=pd.read_csv(GAME_FILE)
lineup_df=pd.read_csv(LINEUP_FILE)
pitch_df=pd.read_csv(PITCH_FILE)


# ======================
# 建立比賽
# ======================

st.header("建立比賽")

date=st.date_input("日期",datetime.today())

opponent=st.text_input("對手")

if st.button("建立新比賽"):

    gid=str(len(game_df)+1)

    new=pd.DataFrame([{

    "比賽ID":gid,
    "日期":date.strftime("%Y-%m-%d"),
    "對手":opponent

    }])

    game_df=pd.concat([game_df,new])

    game_df.to_csv(GAME_FILE,index=False)

    st.success("建立成功")

    st.rerun()



# ======================
# 選擇比賽
# ======================

if game_df.empty:

    st.stop()


game_select=st.selectbox(

"選擇比賽",

game_df["比賽ID"]+" ｜ "+game_df["日期"]+" vs "+game_df["對手"]

)

game_id=game_select.split(" ｜ ")[0]



# ======================
# 先發名單
# ======================

st.header("先發名單")

positions=[

"SS","CF","LF","RF","1B","2B","3B","C","DH","P"

]

names=[]

for i in range(9):

    col1,col2=st.columns(2)

    with col1:

        name=st.text_input(

        f"{i+1}棒",

        key=f"name{i}"

        )

    with col2:

        pos=st.selectbox(

        "守位",

        positions,

        key=f"pos{i}"

        )

    names.append((i+1,name,pos))


pitcher=st.text_input("投手")


if st.button("儲存先發"):

    lineup_df=lineup_df[

    lineup_df["比賽ID"]!=game_id

    ]

    new=[]

    for bat,name,pos in names:

        if name!="":

            new.append({

            "比賽ID":game_id,
            "棒次":bat,
            "姓名":name,
            "守位":pos

            })

    new.append({

    "比賽ID":game_id,
    "棒次":0,
    "姓名":pitcher,
    "守位":"P"

    })

    lineup_df=pd.concat([

    lineup_df,
    pd.DataFrame(new)

    ])

    lineup_df.to_csv(LINEUP_FILE,index=False)

    st.success("先發完成")

    st.rerun()



# ======================
# 局數控制
# ======================

st.divider()

st.header("比賽紀錄")

if "inning" not in st.session_state:

    st.session_state.inning=1

if "half" not in st.session_state:

    st.session_state.half="上"



col1,col2,col3=st.columns(3)

with col1:

    if st.button("◀ 上一局"):

        st.session_state.inning=max(

        1,
        st.session_state.inning-1

        )

with col2:

    st.subheader(

    f"{st.session_state.inning} 局 {st.session_state.half}"

    )

with col3:

    if st.button("下一局 ▶"):

        st.session_state.inning+=1



if st.button("攻守交換"):

    st.session_state.half=(

    "下"

    if st.session_state.half=="上"

    else "上"

    )



# ======================
# 打席
# ======================

st.subheader("打席紀錄")

lineup=lineup_df[

lineup_df["比賽ID"]==game_id

]

if lineup.empty:

    st.info("請先登錄先發")

    st.stop()


batters=lineup[lineup["棒次"]!=0]

bat_select=st.selectbox(

"選擇打者",

batters["姓名"]

)

symbol_col1,symbol_col2=st.columns(2)

with symbol_col1:

    if st.button("O 好球"):

        symbol="O"

    else:

        symbol=None

with symbol_col2:

    if st.button("O/ 揮棒"):

        symbol="O/"

    else:

        symbol=None


col3,col4=st.columns(2)

with col3:

    if st.button("△ 界外"):

        symbol="△"

with col4:

    if st.button("— 壞球"):

        symbol="—"


if symbol:

    new=pd.DataFrame([{

    "比賽ID":game_id,

    "局":st.session_state.inning,

    "上下":st.session_state.half,

    "棒次":bat_select,

    "球數":symbol

    }])

    pitch_df=pd.concat([pitch_df,new])

    pitch_df.to_csv(PITCH_FILE,index=False)

    st.rerun()



# ======================
# 顯示紀錄
# ======================

st.divider()

st.header("本局紀錄")

show=pitch_df[

(pitch_df["比賽ID"]==game_id)&

(pitch_df["局"]==st.session_state.inning)&

(pitch_df["上下"]==st.session_state.half)

]


st.dataframe(show,use_container_width=True)
