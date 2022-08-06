from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome(ChromeDriverManager().install())

def get_page_url(url):
    try:
        data = []
        
        driver.get(url)

        html = driver.page_source

        bs = BeautifulSoup(html,"html.parser")

        bs = bs.find('div', {'class':'cs-list02 cs-list02--ratio small-tp generalRegist'}).find('div', {'class':'list-in'})

        links = bs.find_all('a')
        
        for link in links:
            if 'https://www.kbchachacha.com'+link.get('href') not in data:
                data.append('https://www.kbchachacha.com' + link.get('href'))
    except:
        data = []
    return(data)

urls = get_page_url("https://www.kbchachacha.com/public/search/main.kbc#!?makerCode=122&classCode=2446&carCode=2662&page=3&sort=-orderDate")
print(urls)
print(len(urls))