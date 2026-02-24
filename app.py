import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE="records.csv"

st.title("⚾ 棒球打擊數據系統")

# ========= 讀取 =========

if os.path.exists(FILE):
    records=pd.read_csv(FILE)
else:
    records=pd.DataFrame(columns=[
"日期","球隊","背號","姓名",
"打數","安打","1B","2B","3B","HR",
"BB","SF"
])

# ========= 新增 =========

st.header("新增紀錄")

team=st.text_input("球隊")

number=st.number_input("背號",0)

name=st.text_input("姓名")

AB=st.number_input("打數",0)

H=st.number_input("安打",0)

single=st.number_input("1B",0)

double=st.number_input("2B",0)

triple=st.number_input("3B",0)

HR=st.number_input("HR",0)

BB=st.number_input("BB",0)

SF=st.number_input("SF",0)

if st.button("新增"):

    today=datetime.now().strftime("%Y-%m-%d")

    new=pd.DataFrame([{

"日期":today,
"球隊":team,
"背號":number,
"姓名":name,
"打數":AB,
"安打":H,
"1B":single,
"2B":double,
"3B":triple,
"HR":HR,
"BB":BB,
"SF":SF

}])

    records=pd.concat(
        [records,new],
        ignore_index=True)

    records.to_csv(FILE,index=False)

    st.success("新增成功")

# ========= 累積 =========

st.header("球員累積成績")

if not records.empty:

    summary=records.groupby(
["球隊","背號","姓名"],
as_index=False).sum(numeric_only=True)

    # AVG
    summary["AVG"]=summary.apply(
lambda r:round(r["安打"]/r["打數"],3)
if r["打數"]>0 else 0,
axis=1)

    # SLG
    TB=(
summary["1B"]
+summary["2B"]*2
+summary["3B"]*3
+summary["HR"]*4
)

    summary["SLG"]=(TB/
summary["打數"].replace(0,1)).round(3)

    # OBP
    denominator=(
summary["打數"]
+summary["BB"]
+summary["SF"]
).replace(0,1)

    summary["OBP"]=(
summary["安打"]
+summary["BB"]
)/denominator

    summary["OBP"]=summary["OBP"].round(3)

    # OPS
    summary["OPS"]=(
summary["OBP"]+
summary["SLG"]
).round(3)

    st.dataframe(
summary.sort_values("OPS",ascending=False),
use_container_width=True)

# ========= 原始紀錄 =========

st.header("原始紀錄（單筆刪除）")

if not records.empty:

    st.dataframe(records,use_container_width=True)

    delete_index=st.selectbox(
"選擇刪除紀錄（依序號）",
records.index
)

    if st.button("刪除選定紀錄"):

        records=records.drop(delete_index)

        records.to_csv(FILE,index=False)

        st.success("已刪除")