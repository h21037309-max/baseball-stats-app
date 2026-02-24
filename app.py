import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")

st.title("⚾ 校隊棒球打擊數據系統")

FILE="data.csv"

columns=[

"日期","球隊","對戰球隊","背號","姓名",

"打席","打數","得分","打點","安打",

"1B","2B","3B","HR",

"長打數",

"BB","SF","SH","SB",

"AVG","OBP","SLG","OPS"

]

# ===== CSV =====

if os.path.exists(FILE):

    df=pd.read_csv(FILE)

else:

    df=pd.DataFrame(columns=columns)

# ===== 新增 =====

st.header("新增或累積紀錄")

col1,col2,col3=st.columns(3)

with col1:

    team=st.text_input("球隊")

    number=st.number_input("背號",0)

    name=st.text_input("姓名")

with col2:

    PA=st.number_input("打席",0)

    AB=st.number_input("打數",0)

    R=st.number_input("得分",0)

    RBI=st.number_input("打點",0)

    H=st.number_input("安打",0)

with col3:

    single=st.number_input("1B",0)

    double=st.number_input("2B",0)

    triple=st.number_input("3B",0)

    HR=st.number_input("HR",0)

    BB=st.number_input("BB",0)

    SF=st.number_input("SF",0)

    SH=st.number_input("SH",0)

    SB=st.number_input("SB",0)

# ===== 新增或累計 =====

if st.button("新增或累計"):

    today=datetime.now().strftime("%Y-%m-%d")

    XB=double+triple+HR

    TB=single+double*2+triple*3+HR*4

    AVG=round(H/AB,3) if AB>0 else 0

    OBP=round((H+BB)/(AB+BB+SF),3) if (AB+BB+SF)>0 else 0

    SLG=round(TB/AB,3) if AB>0 else 0

    OPS=round(OBP+SLG,3)

    # 找球員是否存在
    existing=(

        (df["球隊"]==team)&
        (df["背號"]==number)&
        (df["姓名"]==name)

    )

    # ===== 已存在 → 累積 =====

    if existing.any():

        idx=df[existing].index[0]

        df.loc[idx,"日期"]=today

        df.loc[idx,"打席"]+=PA
        df.loc[idx,"打數"]+=AB
        df.loc[idx,"得分"]+=R
        df.loc[idx,"打點"]+=RBI

        df.loc[idx,"安打"]+=H

        df.loc[idx,"1B"]+=single
        df.loc[idx,"2B"]+=double
        df.loc[idx,"3B"]+=triple
        df.loc[idx,"HR"]+=HR

        df.loc[idx,"BB"]+=BB
        df.loc[idx,"SF"]+=SF
        df.loc[idx,"SH"]+=SH
        df.loc[idx,"SB"]+=SB

    # ===== 新球員 =====

    else:

        new=pd.DataFrame([{

"日期":today,
"球隊":team,
"背號":number,
"姓名":name,

"打席":PA,
"打數":AB,
"得分":R,
"打點":RBI,
"安打":H,

"1B":single,
"2B":double,
"3B":triple,
"HR":HR,

"長打數":XB,

"BB":BB,
"SF":SF,
"SH":SH,
"SB":SB,

"AVG":AVG,
"OBP":OBP,
"SLG":SLG,
"OPS":OPS

}])

        df=pd.concat([df,new],ignore_index=True)

    # ===== 全部重新計算 =====

    df["長打數"]=df["2B"]+df["3B"]+df["HR"]

    TB=df["1B"]+df["2B"]*2+df["3B"]*3+df["HR"]*4

    df["AVG"]=df.apply(
lambda r:round(r["安打"]/r["打數"],3)
if r["打數"]>0 else 0,
axis=1)

    df["OBP"]=df.apply(
lambda r:round(
(r["安打"]+r["BB"])/
(r["打數"]+r["BB"]+r["SF"])
,3)
if (r["打數"]+r["BB"]+r["SF"])>0 else 0,
axis=1)

    df["SLG"]=df.apply(
lambda r:round(
(r["1B"]+r["2B"]*2+r["3B"]*3+r["HR"]*4)/
r["打數"]
,3)
if r["打數"]>0 else 0,
axis=1)

    df["OPS"]=(df["OBP"]+df["SLG"]).round(3)

    df.to_csv(FILE,index=False)

    st.success("已累積更新")

# ===== 顯示 =====

st.header("球員累積成績")

if not df.empty:

    show_df=df.sort_values("OPS",ascending=False)

    st.dataframe(
        show_df,
        use_container_width=True
    )

# =====================
# 單筆刪除功能
# =====================

st.header("單筆刪除球員")

if not df.empty:

    # 下拉選球員（不會刪錯）
    options=df.apply(
        lambda r:f"{r['球隊']} - #{int(r['背號'])} {r['姓名']}",
        axis=1
    )

    selected=st.selectbox(
        "選擇要刪除的球員",
        options
    )

    if st.button("❌ 刪除此球員"):

        delete_index=options[options==selected].index[0]

        df=df.drop(delete_index)

        df.to_csv(FILE,index=False)

        st.success("已刪除")

        st.rerun()