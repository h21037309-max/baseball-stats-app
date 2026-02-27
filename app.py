import streamlit as st
import pandas as pd
import os
import uuid
from datetime import datetime

st.set_page_config(layout="wide")

st.title("⚾棒球紀錄系統（穩定完整版）")

TEAM="team.csv"
GAME="games.csv"


# ======================
# 初始化 CSV
# ======================

if not os.path.exists(TEAM):

    pd.DataFrame(columns=[
        "player_id",
        "姓名",
        "背號"
    ]).to_csv(TEAM,index=False)


if not os.path.exists(GAME):

    pd.DataFrame(columns=[
        "game_id",
        "日期",
        "對手"
    ]).to_csv(GAME,index=False)


team=pd.read_csv(TEAM)

games=pd.read_csv(GAME)



# ======================
# 球員管理
# ======================

st.header("👥 球員名單管理")

name=st.text_input("姓名")

number=st.number_input("背號",0,999,0)


if st.button("新增球員"):

    if name!="":

        new=pd.DataFrame([{

        "player_id":str(uuid.uuid4()),
        "姓名":name,
        "背號":number

        }])

        team=pd.concat([team,new],ignore_index=True)

        team.to_csv(TEAM,index=False)

        st.success("新增成功")

        st.rerun()



st.subheader("目前球員")


if team.empty:

    st.info("尚無球員")

else:

    team=team.reset_index(drop=True)

    for idx,r in team.iterrows():

        col1,col2=st.columns([9,1])

        col1.write(f"#{int(r['背號'])}  {r['姓名']}")

        # ⭐唯一KEY 防爆炸
        delete_key=f"delete_{idx}_{r['背號']}"

        if col2.button("刪除",key=delete_key):

            team=team.drop(idx)

            team.to_csv(TEAM,index=False)

            st.success("已刪除")

            st.rerun()



# ======================
# 建立比賽
# ======================

st.divider()

st.header("⚾ 建立新比賽")

game_date=st.date_input(

"比賽日期",

datetime.today()

)

enemy=st.text_input("對手球隊")


if st.button("建立比賽"):

    if enemy=="":

        st.warning("請輸入對手")

    else:

        new_game=pd.DataFrame([{

        "game_id":str(uuid.uuid4()),

        "日期":game_date.strftime("%Y-%m-%d"),

        "對手":enemy

        }])

        games=pd.concat([games,new_game],ignore_index=True)

        games.to_csv(GAME,index=False)

        st.success("建立成功")

        st.rerun()



# ======================
# 比賽列表
# ======================

st.divider()

st.header("📅 比賽列表")


games=pd.read_csv(GAME)


if games.empty:

    st.info("尚未建立比賽")

else:

    games=games.reset_index(drop=True)

    for idx,r in games.iterrows():

        col1,col2=st.columns([9,1])

        col1.write(

        f"{r['日期']} VS {r['對手']}"

        )

        delete_key=f"delete_game_{idx}"

        if col2.button(

        "刪除",

        key=delete_key

        ):

            games=games.drop(idx)

            games.to_csv(GAME,index=False)

            st.success("比賽刪除")

            st.rerun()



# ======================
# 下階段提示
# ======================

st.divider()

st.info("""

下一步將加入：

✔ 先發1~9棒設定  
✔ 投手  
✔ 攻守交換  
✔ 逐球紀錄表  

""")
