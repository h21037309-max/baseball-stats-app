import streamlit as st
from google.cloud import vision
from PIL import Image
import pandas as pd
import io
import re
import uuid
import os


TEAM_FILE="team_players.csv"


st.title("📸 名冊拍照匯入球員")


# ========= 上傳 =========

tab1,tab2=st.tabs(["📸 拍照","📂 上傳"])


image=None

with tab1:

    image=st.camera_input("拍攝紙本名冊")


with tab2:

    upload=st.file_uploader("上傳圖片",type=["jpg","png","jpeg"])

    if upload:

        image=upload



# ========= OCR =========

def ocr_text(img):

    client=vision.ImageAnnotatorClient()

    content=img.read()

    image=vision.Image(content=content)

    response=client.text_detection(image=image)

    texts=response.text_annotations

    if not texts:

        return ""

    return texts[0].description



# ========= 辨識 =========

if image:

    st.image(image,width=400)

    if st.button("開始辨識"):

        with st.spinner("OCR 辨識中..."):

            text=ocr_text(image)

        st.session_state["ocr_raw"]=text



# ========= 解析 =========

if "ocr_raw" in st.session_state:

    st.subheader("OCR文字")

    st.text_area(

    "辨識結果",

    st.session_state["ocr_raw"],

    height=200

    )


    raw=st.session_state["ocr_raw"]


    # ⭐ 背號 姓名

    pattern=r"(\d{1,3})\s*([一-龥]{2,4})"


    matches=re.findall(pattern,raw)


    if matches:

        st.success(f"辨識到 {len(matches)} 位球員")


        data=[]

        for num,name in matches:

            data.append({

            "player_id":str(uuid.uuid4()),

            "背號":int(num),

            "姓名":name

            })


        df=pd.DataFrame(data)


        st.subheader("確認球員")

        edited=st.data_editor(

        df,

        num_rows="dynamic",

        use_container_width=True

        )


        # ========= 匯入 =========

        if st.button("✅ 匯入球員"):

            if os.path.exists(TEAM_FILE):

                old=pd.read_csv(TEAM_FILE)

                new=pd.concat([old,edited])

            else:

                new=edited


            new.to_csv(TEAM_FILE,index=False)


            st.success("匯入完成")

            st.balloons()

            del st.session_state["ocr_raw"]

            st.rerun()

    else:

        st.error("沒有辨識到背號與姓名")
