import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")

st.title("⚾ 棒球打擊數據庫")

FILE="data.csv"

# ========= 登入 =========

st.sidebar.title("登入")

users={

"洪仲平":"8610",

"王小明":"1111",

"陳志豪":"2222",

"邱珈琪":"0000",

"黃李孟蓁":"1109"

}

ADMIN="洪仲平"

username=st.sidebar.text_input("帳號")

password=st.sidebar.text_input(
"密碼",
type="password"
)

if username not in users or users[username]!=password:

    st.warning("左上角登入")

    st.stop()

# ========= 欄位 =========

columns=[

"日期","球隊","背號","姓名",

"對戰球隊","投手",

"打席","打數","得分","打點","安打",

"1B","2B","3B","HR",

"BB","SF","SH","SB"

]

# ========= CSV =========

if os.path.exists(FILE):

    df=pd.read_csv(FILE)

else:

    df=pd.DataFrame(columns=columns)

# ========= 基本資料 =========

st.header("球員基本資料")

colA,colB=st.columns(2)

with colA:

    team=st.text_input("球隊")

with colB:

    number=st.number_input("背號",0)

if username==ADMIN:

    name=st.text_input("姓名")

else:

    name=username

    st.write(f"球員：{name}")

# ========= 新增比賽 =========

st.header("新增比賽紀錄")

c1,c2,c3=st.columns(3)

with c1:

    opponent=st.text_input("對戰球隊")

    pitcher=st.selectbox(
        "投手",
        ["左投","右投"]
    )

with c2:

    PA=st.number_input("打席",0)

    AB=st.number_input("打數",0)

    R=st.number_input("得分",0)

    RBI=st.number_input("打點",0)

    H=st.number_input("安打",0)

with c3:

    single=st.number_input("1B",0)

    double=st.number_input("2B",0)

    triple=st.number_input("3B",0)

    HR=st.number_input("HR",0)

    BB=st.number_input("BB",0)

    SF=st.number_input("SF",0)

    SH=st.number_input("SH",0)

    SB=st.number_input("SB",0)

# ========= 新增 =========

if st.button("新增紀錄"):

    today=datetime.now().strftime("%Y-%m-%d")

    new=pd.DataFrame([{

"日期":today,
"球隊":team,
"背號":number,
"姓名":name,

"對戰球隊":opponent,
"投手":pitcher,

"打席":PA,
"打數":AB,
"得分":R,
"打點":RBI,
"安打":H,

"1B":single,
"2B":double,
"3B":triple,
"HR":HR,

"BB":BB,
"SF":SF,
"SH":SH,
"SB":SB

}])

    df=pd.concat([df,new],ignore_index=True)

    df.to_csv(FILE,index=False)

    st.success("新增成功")

# ========= 顯示 =========

st.header("比賽紀錄")

if not df.empty:

    if username==ADMIN:

        player_df=df

    else:

        player_df=df[df["姓名"]==username]

    # ===== Excel加總 =====

    total=player_df.sum(numeric_only=True)

    TB=(

total["1B"]
+total["2B"]*2
+total["3B"]*3
+total["HR"]*4

)

    AB_total=total["打數"]

    H_total=total["安打"]

    AVG=round(H_total/AB_total,3) if AB_total>0 else 0

    OBP=round(
(H_total+total["BB"])/
(AB_total+total["BB"]+total["SF"])
,3) if (AB_total+total["BB"]+total["SF"])>0 else 0

    SLG=round(TB/AB_total,3) if AB_total>0 else 0

    OPS=round(OBP+SLG,3)

    st.subheader("累積統計")

    m1,m2,m3,m4=st.columns(4)

    m1.metric("打席",int(total["打席"]))

    m2.metric("安打",int(H_total))

    m3.metric("AVG",AVG)

    m4.metric("OPS",OPS)

    # ===== 表格 =====

    st.subheader("每場紀錄")

    show_df=player_df.sort_values("日期",ascending=False)

    for idx,row in show_df.iterrows():

        col1,col2=st.columns([8,1])

        with col1:

            st.write(

f"{row['日期']} | {row['對戰球隊']} | {row['投手']} | AB:{row['打數']} H:{row['安打']}"

            )

        with col2:

            if st.button("❌",key=f"del{idx}"):

                df=df.drop(idx)

                df.to_csv(FILE,index=False)

                st.success("已刪除")

                st.rerun()