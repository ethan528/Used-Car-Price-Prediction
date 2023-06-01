import streamlit as st
from PIL import Image
import pandas as pd 
from time import time
df = pd.read_csv('usedcar_total_0608.csv')



st.set_page_config(layout="wide")

st.image('lemon.png', width=100)
st.title("PINK-LEMON")



nation = st.sidebar.selectbox("국산/수입", tuple(df['nation'].unique()))
car_brand = st.sidebar.selectbox("제조사", tuple(sorted(df[df['nation']==nation]['car_brand'].unique())))
car_model = st.sidebar.selectbox("차량모델", tuple(sorted(df[df['car_brand']==car_brand]['car_model'].unique())))
car_type = st.sidebar.selectbox("차종", tuple(sorted(df[df['car_model']==car_model]['car_type'].unique())))
fuel = st.sidebar.selectbox("연료", tuple(sorted(df['fuel'].unique())))

new_car = st.sidebar.number_input("신차가격을 '만원'단위 숫자만 입력해주세요",min_value=0,step=100,help='7,800만원 >> 7800 입력')
year = st.sidebar.selectbox("연식", tuple(sorted(df['year'].unique())))
use = st.sidebar.number_input("사용개월 수를 '개월'단위 숫자만 입력해주세요",min_value=0,step=1,help='2년 3개월 >> 27 입력')
mileage = st.sidebar.number_input("주행거리를 'Km'단위 숫자만 입력해주세요",min_value=0,step=1000,help='50,400km >> 50400 입력')
change = st.sidebar.number_input("사용자 변경 수 '횟수'단위 숫자만 입력해주세요",min_value=0,step=1,help='4회 >> 4 입력')
trans = st.sidebar.selectbox("변속기", tuple(sorted(df['trans'].unique())))
loss = st.sidebar.selectbox("전손이력", ("없음", "있음"))
flood = st.sidebar.selectbox("침수이력", ("없음", "있음"))
usage = st.sidebar.selectbox("용도이력", ("없음", "있음"))
insurance = st.sidebar.selectbox("보험사고", ("없음", "있음"))
pred_button = st.sidebar.button("Predict")

st.write(f'검색옵션: {nation}/{car_brand}/{car_model}/{car_type}/{fuel}/{trans}/신차가격: {new_car}/{year}년식/사용개월{use}/주행거리{mileage}km/사용자변경:{change}회/전손:{loss}/침수:{flood}/용도:{usage}/보험사고:{insurance}')

# 사이드바 크기 조정
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 350px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 450px;
        margin-left: -450px;
        }
        </style>
        """,
    unsafe_allow_html=True)

# 메인화면 레이아웃 설정하기

if pred_button == True:

    col1, col2 = st.columns(2)

    # 레이아웃 1
    with col1:
        st.subheader("신차대비 중고차 감가상각률 예측")



    # 레이아웃 2
    with col2:
        st.subheader("검색 중고차 관련 정보")

    
    if st.sidebar.button('초기화') == True:
        with st.spinner(text="In progress..."):
            time.sleep(1.5)
            st.experimental_rerun() 
        
    else:
        pass

else :
    pass

