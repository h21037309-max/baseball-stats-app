import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide")

st.title("⚾ 棒球打擊數據系統")

FILE="data.csv"

# ===== CSV讀取 =====

if os.path.exists(FILE):
    df=pd.read_csv(FILE)
else:
    df=pd.DataFrame()

# ===== 新增紀錄 =====

st.header("新增比賽紀錄")

col1,col2,col3=st.columns(3)

with col1:

    team=st.text_input("球隊")

    opponent=st.text_input("對戰球隊")

    number=st.number_input("背號",0)

    name=st.text_input("姓名")

    pitcher=st.selectbox(
    "投手",
    ["左投","右投"]
    )

with col2:

    PA=st.number_input("打席",0)

    AB=st.number_input("打數",0)

    R=st.number_input("得分",0)

    RBI=st.number_input("打點",0)

    H=st.number_input("安打",0)

with col3:

    single=st.number_input("一壘安打",0)

    double=st.number_input("二壘安打",0)

    triple=st.number_input("三壘安打",0)

    HR=st.number_input("全壘打",0)

    BB=st.number_input("四壞",0)

    SF=st.number_input("高飛犧牲打",0)

    SH=st.number_input("犧牲短打",0)

    SB=st.number_input("盜壘",0)

# ===== 新增 =====

if st.button("新增紀錄"):

    date=datetime.now()

    XB=double+triple+HR

    AVG=round(H/AB,3) if AB>0 else 0

    OBP=round((H+BB)/(AB+BB+SF),3) if (AB+BB+SF)>0 else 0

    TB=single+double*2+triple*3+HR*4

    SLG=round(TB/AB,3) if AB>0 else 0

    OPS=round(OBP+SLG,3)

    new=pd.DataFrame([{

"日期":date,
"球隊":team,
"對戰球隊":opponent,
"背號":number,
"姓名":name,
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

    df.to_csv(FILE,index=False)

    st.success("已儲存")

# ===== 顯示資料 =====

st.header("全部比賽紀錄")

if not df.empty:

    st.dataframe(df,use_container_width=True)

# ===== 左投右投分析 =====

st.header("左投 vs 右投 OPS")

if not df.empty:

    analysis=df.groupby(
        ["姓名","投手"]
    )[["打席","安打"]].sum().reset_index()

    st.dataframe(analysis,use_container_width=True)