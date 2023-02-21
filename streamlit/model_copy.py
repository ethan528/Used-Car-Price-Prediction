import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib import font_manager
import numpy as np
import seaborn as sns
import joblib
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster
from collections import defaultdict
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
import math
# from wordcloud import WordCloud
from PIL import Image


scaler = joblib.load('s_scale_0608.pkl')
xgb_reg = joblib.load("xgb_reg_0608.pkl")
rand_reg = joblib.load('randforest_0608.pkl')
df = pd.read_csv(
    './usedcar_total_0608.csv')
search_car = pd.read_csv('./search_vector_0608.csv')

font_path = "/Library/Fonts/a포트폴리오M.otf"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family = font)


def Make_sample(use, nation, brand, model, mileage, year, type, fuel, trans, loss, flood, usage, change, insurance, new_car):
    # global search_car
    for i, column in enumerate(search_car.columns):
        if i <= 3:
            search_car[column][0] = 0
        else:
            search_car[column][0] = np.uint8(0)

    search_car['use'] = use
    search_car['mileage'] = mileage
    search_car['year'] = year
    search_car['change'] = change

    search_car[f'nation_{nation}'] = np.uint8(1)
    search_car[f'car_brand_{brand}'] = np.uint8(1)
    search_car[f'car_model_{model}'] = np.uint8(1)
    search_car[f'car_type_{type}'] = np.uint8(1)
    search_car[f'fuel_{fuel}'] = np.uint8(1)
    search_car[f'trans_{trans}'] = np.uint8(1)
    search_car[f'loss_{loss}'] = np.uint8(1)
    search_car[f'flood_{flood}'] = np.uint8(1)
    search_car[f'usage_{usage}'] = np.uint8(1)
    search_car[f'insurance_{insurance}'] = np.uint8(1)

    scaled_X = scaler.transform(search_car)

    Predict(scaled_X, new_car)
    return scaled_X


def Predict(scaled_X, new_car):
    prediction = xgb_reg.predict(scaled_X)
    prediction2 = rand_reg.predict(scaled_X)

    model_dep = round(prediction[0].astype('float64'), 1)
    model_dep2 = round(prediction2[0].astype('float64'), 1)

    print(prediction)
    st.success(f'해당 차량의 감가상각률은 {round((prediction[0] + prediction2[0])/2)}% 입니다.')
    # st.metric(label="감가상각률", value=f"{(prediction[0] + prediction2[0])/2}%")
    Calculate(model_dep, model_dep2, int(new_car))
    return prediction


def Calculate(model_dep, model_dep2, new_car):
    model_price = [math.trunc(new_car * (100 - (int(math.ceil(model_dep))))/100),
                   math.ceil(new_car * (100 - (int(math.trunc(model_dep))))/100)]
    model_price2 = [math.trunc(new_car * (100 - (int(math.ceil(model_dep2))))/100),
                    math.ceil(new_car * (100 - (int(math.trunc(model_dep2))))/100)]
    price_min = (model_price[0]+model_price2[0])/2
    price_max = (model_price[1]+model_price2[1])/2
    # st.success(f'해당 차량의 예상 가격은 {price_min} - {price_max} 만원입니다.')
    st.metric(label="예상 가격", value=f"{math.trunc(price_min)} - {math.ceil(price_max)} 만원")
    return model_price


def show_map(model, lat=36.24, lng=128):
    search_car_list = df[df['car_model'] == model].index
    center = [lat, lng]
    m = folium.Map(location=center,
                   zoom_start=7.3,
                   width=700,
                   height=565,
                   tiles='cartodbpositron')

    cluster = MarkerCluster().add_to(m)
    for car_idx in search_car_list:
        folium.Marker(location=[df['lat'][car_idx], df['lng'][car_idx]],
                      tooltip=df['sales_corp'][car_idx],
                      popup=f"<pre>{df['car_model'][car_idx]}{df['name_detailed'][car_idx]}</pre><pre>번호판: {df['car_no'][car_idx]} 가격: {df['price'][car_idx]}만원</pre>",
                      icon=folium.Icon(icon='Car', color='red')).add_to(cluster)

    m.save(f'{model}.html')
    return m


def main():

    # 페이지 레이아웃 설정
    st.set_page_config(
        page_title="PINK-LEMON",
        page_icon="🍋",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.image('./lemon.png', width=100)
    st.title("PINK-LEMON")

    # selectbox 변수들 설정
    차종 = [f"{typpe}" for typpe in sorted(df.car_type.unique())]
    bm = defaultdict(set)
    bm1 = defaultdict(set)
    for row in df.values:
        bm1[f'{row[4]}'].add(f'{row[3]}')
    국산수입_제조사 = dict(bm1)
    국산수입 = [f"{nation}" for nation in 국산수입_제조사.keys()]
    for row in df.values:
        bm[f'{row[3]}'].add(f'{row[5]}')
    제조사_모델 = dict(bm)
    제조사 = [f"{brand}" for brand in 제조사_모델.keys()]
    연식 = [f"{year}" for year in sorted(df.year.unique())]
    지역 = [f"{local}" for local in sorted(df.car_area.unique())]
    연료 = [f"{fuel}" for fuel in sorted(df.fuel.unique())]
    opt = 국산수입, 차종, 제조사, 연식, 지역, 연료
    dft = '선택해주세요'
    for o in opt:
        o.insert(0, dft)

    # 초기화버튼
    if st.sidebar.button('초기화'):
        st.experimental_rerun()

    # 사이드바
    nation = st.sidebar.selectbox("국산/수입", 국산수입)
    if nation != dft:
        brand = st.sidebar.selectbox(
            "제조사", [f"{brand}" for brand in 국산수입_제조사[f"{nation}"]])
        if brand != dft:
            model = st.sidebar.selectbox(
                "모델", [f"{model}" for model in 제조사_모델[f"{brand}"]])
    type = st.sidebar.selectbox("차종", 차종)
    year = st.sidebar.selectbox("연식", 연식)
    new_car = st.sidebar.number_input("신차가격", help="단위 : 만원", min_value=0)
    use = st.sidebar.number_input(
        "사용 개월 수를 입력해주세요", help="월단위로 숫자만 입력해주세요 ex) 12개월=12", min_value=0)
    mileage = st.sidebar.number_input(
        "주행거리를 입력해주세요", help="km단위로 숫자만 입력해주세요 ex) 12km=12", min_value=0)
    change = st.sidebar.number_input(
        "소유주 변경횟수를 입력해주세요", help="숫자만 입력해주세요 ex) 12회=12", min_value=0)
    fuel = st.sidebar.selectbox("연료", 연료)
    trans = st.sidebar.selectbox("변속기", ("오토", "수동", "기타", "SAT", "CVT"))
    loss = st.sidebar.selectbox("전손이력", ("없음", "있음"))
    flood = st.sidebar.selectbox("침수이력", ("없음", "있음"))
    usage = st.sidebar.selectbox("용도이력", ("없음", "있음"))
    insurance = st.sidebar.selectbox("보험사고", ("없음", "있음"))
    

    # 사이드바 크기 조정
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            width: 450px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            width: 500px;
            margin-left: -500px;
            }
            </style>
            """,
        unsafe_allow_html=True)

    # 예측 시작
    predi = st.sidebar.button("Predict")
    if predi:
        st.write(f'검색옵션: {nation}/{brand}/{model}/{type}/{fuel}/{trans}/신차가격: {new_car}/{year}년식/사용개월{use}/주행거리{mileage}km/사용자변경:{change}회/전손:{loss}/침수:{flood}/용도:{usage}/보험사고:{insurance}')
        # 메인 화면 레이아웃 설정하기
        col1, col2 = st.columns(2)

        with col1:

            # 감가상각률 예측 타이틀

            st.header("차량 감가상각률 예측")
            Make_sample(use, nation, brand, model, mileage, year, type,
                                fuel, trans, loss, flood, usage, change, insurance, new_car)
            if model:
                dfdf = df[(df['car_brand'].str.contains(f'{brand}')) & (df['car_model'].str.contains(f'{model}'))]
                with st.expander("매물 정보"):
                    st.dataframe(dfdf)
                    st.text(f"{len(dfdf)} 대의 매물이 존재합니다.")

            st.header("매물 지도")
            show_map(model, lat=36.24, lng=128)
            HtmlFile = open(f"{model}.html", 'r', encoding='utf-8')
            source_code = HtmlFile.read()
            components.html(source_code, width=700, height=565)

            with st.expander("검색 모델 가격 상관관계"):
                fig, ax = plt.subplots()
                feature = ['price','new_price', 'depreciation', 'mileage','year','use','change']
                heat_table = dfdf[feature].corr()
                mask = np.zeros_like(heat_table)
                mask[np.triu_indices_from(mask)] = True
                
                heatmap_ax = sns.heatmap(heat_table, annot=True, mask = mask, cmap='YlOrRd',linewidths=0.5, ax = ax)
                heatmap_ax.set_xticklabels(heatmap_ax.get_xticklabels(), fontsize=7 , rotation =30)
                heatmap_ax.set_yticklabels(heatmap_ax.get_yticklabels(), fontsize=7)
                
                st.pyplot(fig)

        with col2:

            # 워드클라우드 파트 타이틀
            st.header("모델 관련 정보")
            # 워드클라우드
            with st.expander("긍정"):
                try:
                    image = Image.open(
                        f'./wordcloud/{brand}/{brand}+{model}+긍정.jpg')
                    st.image(image)
                except:
                    st.write("정보가 부족합니다")

            with st.expander("부정"):
                try:
                    image = Image.open(
                        f'./wordcloud/{brand}/{brand}+{model}+부정.jpg')
                    st.image(image)
                except:
                    st.write("정보가 부족합니다")
                
            # 긍부정 파이차트

            try:
                image = Image.open(
                        f'./wordcloud/{brand}/{brand}+{model}+긍정.jpg')
                emo_df = pd.read_csv('./preprocessed_emotion_labeled_youtube_0607.csv')
                df2 = emo_df[(emo_df['car_brand'].str.contains(f'{brand}')) & (
                        emo_df['car_model'].str.contains(f'{model}'))]
                data= [len(df2[df2['emotion'] == 0]),len(df2[df2['emotion'] == 1]),len(df2[df2['emotion'] == -1])]
                labels = ['긍정','부정','궁금']
                colors = ['#ffc000','#ff9999','#9370db']
                explode = [0.05 for x in range(len(data))]

                fig, ax = plt.subplots()

                plt.figure(figsize=(10,10))
                plt.title('긍정/부정 비율', fontsize = 20)
                ax.pie(data,
                        labels = labels,
                        autopct='%.1f%%',
                    startangle = 90,
                    counterclock=False,
                    textprops = {'fontsize':22}, shadow=True, colors = colors, explode = explode)
                ax.axis('equal')
                # ax.figure(figsize=(10,10))
                with st.expander('긍정/부정 비율'):
                    st.pyplot(fig)
            except:
                with st.expander("긍정/부정 비율"):
                    st.write("정보가 부족합니다.")
                    
        # 모델 관련 뉴스 정보 제공 타이틀
            if brand == '한국GM':
                brand = '쉐보레'
            if brand == '르노코리아':
                brand = '르노삼성'
            if brand == '제네시스':
                brand = '현대'
            df_article = pd.read_csv(
                f'./articles/{brand}_articles.csv')

            st.header("관련 뉴스")
            with st.expander("뉴스 보기"):
                st.markdown(
                    f"[{df_article['title'].loc[0]}]({df_article['url'].loc[0]})")
                st.markdown(
                    f"[{df_article['title'].loc[1]}]({df_article['url'].loc[1]})")
                st.markdown(
                    f"[{df_article['title'].loc[2]}]({df_article['url'].loc[2]})")
                st.markdown(
                    f"[{df_article['title'].loc[3]}]({df_article['url'].loc[3]})")
                st.markdown(
                    f"[{df_article['title'].loc[4]}]({df_article['url'].loc[4]})")


if __name__ == '__main__':
    main()
