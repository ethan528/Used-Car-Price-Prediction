from attr import NOTHING
from bs4 import BeautifulSoup
from regex import D
import requests
import re

from sqlalchemy import null

def get_data(url):
    try:
        #headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        #res = requests.get(url, headers = headers)
        res = requests.get(url)
        bs = BeautifulSoup(res.text,'html.parser')
        data = []
        
        ################ 차명####################
        name = bs.find('div', {'class':'car-buy-price'}).find('strong', {'class':'car-buy-name'}).text
        name_partition = name.partition(')')
        
        ################ 가격####################
        car_price = bs.find('div', {'class':'car-buy-price'})
        for dd in car_price:
            price = bs.find('dd').text.strip('\n')
        
        ################연식, 주행거리, 연료, 판매위치 ####################
        car_buy_share = bs.find('div', {'class':'car-buy-share'})
        for txt_info in car_buy_share:
            info = bs.find('div', {'class':'txt-info'}).text
            year = info.split('\n')[1]
            km = info.split('\n')[2]
            oil = info.split('\n')[3]
            location = info.split('\n')[4]       
        
        ################ 차번호, 변속기, 차종, 배기량, 색상, 세금미납, 압류 ####################
        detail_info_table = bs.find('table', {'class':'detail-info-table'}).find_all('td')
        num = detail_info_table[0].text
        transmission = detail_info_table[4].text       
        type = detail_info_table[6].text
        engine_capacity = detail_info_table[7].text.strip('cc')
        color = detail_info_table[8].text
        tax_default = detail_info_table[9].text.strip('\n')
        repossession = detail_info_table[10].text.strip('\n')

    
        ################ 주행거리(설명) ####################
        km_words = bs.find('div', {'class':'info-txt mg-t20'}).find_all('span')
        km_words = km_words[3].text
        
        ################ 사고횟수 ####################
        accident_num = bs.find('div', {'class':'car-buy-state'}).find_all('span')[3].text
        for accident in accident_num:
            if len(accident_num) > 3:
                accident = bs.find('div', {'class':'car-buy-state'}).find_all('span')[2].text
            else:
                accident = bs.find('div', {'class':'car-buy-state'}).find_all('span')[3].text
        
        ################ 소유자변경 ####################
        owner_changed = bs.find('div', {'class':'mg-t40'}).find_all('dd')[3].text
        owner_change = re.sub('\n|\t|\r|','',owner_changed)

        
        ################ 차체보증 (브랜드 보증)####################
        car_warranty = bs.find('div', {'class':'ln02'}).findAll('div', {'class':'box-txt'})[0].text
        
        ################ 엔진보증 (브랜드 보증)####################
        engine_warranty = bs.find('div', {'class':'ln02'}).findAll('div', {'class':'box-txt'})[1].text
        
        ################ 차량 판매위치 상세 ####################
        차량판매정보_상세 = bs.find('div', {'class':'map-txt'}).find_all('p') 
        차량판매_상사명 = 차량판매정보_상세[0].text.strip('상사명 :')
        차량판매_위치 = 차량판매정보_상세[1].text.strip('주소 : ')
        
        ################ 보험 보증 ####################
        보험_보증_km = bs.find('div', {'class':'gt-pos'}).find_all('strong')[0].text
        보험_보증 = bs.find('div', {'class':'gt-pos'}).find_all('strong')[1].text
        
        ################ 판매자 설명 ####################
        판매자_설명 = bs.find('div', {'class':'dealer-info'}).text
        
        ################시세정보 ####################
        시세_안전구간 = bs.find('div', {'class':'m-price-list01'}).find_all('strong')[0].text
        시세_안전지수 = bs.find('div', {'class':'m-price-list01'}).find_all('strong')[2].text

        ################침수정보 ####################
        drown = bs.find('div', {'class':'mg-t40'}).find_all('strong')[1].text
        


        
        data.append(name_partition[2])
        data.append(price)
        data.append(location)
        data.append(num)
        data.append(km)
        data.append(km_words)
        data.append(accident)
        data.append(transmission)
        data.append(color)
        data.append(engine_capacity)
        data.append(type)
        data.append(year)
        data.append(oil)
        data.append(owner_change)  
        data.append(repossession)
        data.append(tax_default)    
        data.append(car_warranty)
        data.append(engine_warranty)
        data.append(차량판매_상사명)
        data.append(차량판매_위치)
        data.append(보험_보증_km)
        data.append(보험_보증)
        data.append(판매자_설명)
        data.append(시세_안전구간)
        data.append(시세_안전지수)
        data.append(drown)

        try:
            외부패널 = bs.find('div', {'class':'dia-list clearFix'}).find('dl', {'id':'diagResultPanelList'}).find_all('strong')
            프레임 = bs.find('div', {'class':'dia-list clearFix'}).find('dl', {'id':'diagResultFrameList'}).find_all('strong')
            for i in 외부패널:
                data.append(i.text)
            for i in 프레임:
                data.append(i.text)

        except:
            for i in range(11):
                data.append(None)
        
        example1 = bs.find('h2', {'class':'title'}).text
        data.append(example1)

    except AttributeError or IndexError:
        data.append(None)
        pass

    except Exception as e:
        print(e)
        pass

    return data

# def convert_to_df(self, data):
#     empty_df = pd.DataFrame(index=range(0,0), columns = ['name','price','location','num','km','km_word', 'accident','transmission', 'color','engine_capacity','type','year','oil', 'owner_change', 'drown', 'repossession', 'tax_default', 'warranty', 'engine_warranty'])
#     df = empty_df.append(pd.Series(data,index=empty_df.columns), ignore_index=True)
#     return df

k = get_data("https://www.kbchachacha.com/public/car/detail.kbc?carSeq=22285250")

#KB진단 예시
#k = get_data("https://www.kbchachacha.com/public/car/detail.kbc?carSeq=22280012")
#k = get_data("https://www.kbchachacha.com/public/car/detail.kbc?carSeq=22282954")

print(k)
print(len(k))