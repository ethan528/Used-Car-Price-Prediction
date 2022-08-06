# 라이브러리


import streamlit as st
import pandas as pd
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import defaultdict
import random
import streamlit.components.v1 as components


# 타이틀


st.set_page_config(
     page_title="PINK-LEMON",
     page_icon="🍋",
     layout="wide",
     initial_sidebar_state="expanded"
 )

st.title("PINK-LEMON")


# 사이드바


if st.sidebar.button('초기화'):
    st.experimental_rerun()

df = pd.read_csv('C:/Users/USER/TIL/중고차 시세 예측/preprocessed_total_0529.csv', encoding='ansi')

df = df.sort_values('car_brand')

차종 = [f"{typpe}" for typpe in sorted(df.car_type.unique())]
bm = defaultdict(set)
for row in df.values:
    bm[f'{row[3]}'].add(f'{row[4]}')
제조사_모델 = dict(bm)
제조사 = [f"{brand}" for brand in 제조사_모델.keys()]
지역 = [f"{local}" for local in sorted(df.car_area.unique())]
연료 = [f"{fuel}" for fuel in sorted(df.fuel.unique())]
opt = 차종, 제조사, 지역, 연료
dft = '선택해주세요'
for o in opt:
    o.insert(0, dft)

type_sb = st.sidebar.selectbox("차종", 차종)
brand_sb = st.sidebar.selectbox("제조사", 제조사)
if brand_sb != dft:
    model_sb = st.sidebar.selectbox("모델", [f"{model}" for model in 제조사_모델[f"{brand_sb}"]])
else:
    model_sb = st.sidebar.selectbox("모델", ("제조사를 선택해주세요", ""), disabled=True)
year_sb = st.sidebar.text_input("연식을 입력해주세요", help="숫자만 입력해주세요 ex) 12년식=12")
change_sb = st.sidebar.text_input("소유주 변경횟수를 입력해주세요", help="숫자만 입력해주세요 ex) 12회=12")
use_sb = st.sidebar.text_input("사용 개월 수를 입력해주세요", help="월단위로 숫자만 입력해주세요 ex) 12개월=12")
mileage_sb = st.sidebar.text_input("주행거리를 입력해주세요", help="km단위로 숫자만 입력해주세요 ex) 12km=12")
local_sb = st.sidebar.selectbox("지역", 지역)
fuel_sb = st.sidebar.selectbox("연료", 연료)
trans_sb = st.sidebar.selectbox("변속기", ("오토", "수동", "기타", "SAT", "CVT"))
loss_sb = st.sidebar.selectbox("전손이력", ("정보없음", "없음", "있음"))
flood_sb = st.sidebar.selectbox("침수이력", ("정보없음", "없음", "있음"))
usage_sb = st.sidebar.selectbox("용도이력", ("정보없음", "없음", "있음"))
insurance_sb = st.sidebar.selectbox("보험사고", ("없음", "있음"))


# 메인화면


left, right = st.columns(2)

with left:

    st.subheader("left")

    #if model_sb:
    #    dfdf = df[(df['car_brand'].str.contains(f'{brand_sb}'))&(df['car_name'].str.contains(f'{model_sb}'))]
    #    st.dataframe(dfdf)
    dataframe = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40],
     'third column': [100, 200, 300, 400],
     'forth column': [1000, 2000, 3000, 4000]
    })
    st.experimental_show(dataframe)

with right:

    st.subheader(f"{brand_sb} 관련 뉴스")

    #news_df = pd.read_csv(f"./{국산/수입}차_articles/{brand_sb}_articles.csv")
    news_df = pd.read_csv("./수입차_articles/포르쉐_articles.csv")

    news_title = news_df.title.tolist()
    random.shuffle(news_title)
    news_title = news_title[3:8]

    news_url = [url for title in news_title for url in news_df[news_df["title"] == title].url]

    st.markdown(f"[1. {news_title[0]}]({news_url[0]})")
    st.markdown(f"[2. {news_title[1]}]({news_url[1]})")
    st.markdown(f"[3. {news_title[2]}]({news_url[2]})")
    st.markdown(f"[4. {news_title[3]}]({news_url[3]})")
    st.markdown(f"[5. {news_title[4]}]({news_url[4]})")

    st.subheader(f"{model_sb} 관련 키워드")

    with st.expander("긍정"):
        try:
            image_pos = Image.open(f'./wordcloud/{brand_sb}/{brand_sb}+{model_sb}+긍정.jpg')
            st.image(image_pos, width=450)
        except FileNotFoundError:
            st.text("준비중입니다")

    with st.expander("부정"):
        try:
            image_neg = Image.open(f'./wordcloud/{brand_sb}/{brand_sb}+{model_sb}+부정.jpg')
            st.image(image_neg, width=450)
        except FileNotFoundError:
            st.text("준비중입니다")
    
one, two, three = st.columns(3)

with one:
    HtmlFile = open("sample.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code,height = 1000)

    image = Image.open('./wordcloud.jpg')
    st.image(image, width=340)

with two:
    dataframe = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40],
     'third column': [100, 200, 300, 400],
     'forth column': [1000, 2000, 3000, 4000]
    })
    st.experimental_show(dataframe)

with three:
    image = Image.open('./wordcloud2.png')
    st.image(image, width=340)
