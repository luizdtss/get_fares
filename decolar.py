
import time
from datetime import date,timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

    #--------------------------------------------------------Parâmetros da pesquisa--------------------------------------------------------#

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(chrome_options=options, executable_path="/Users/Luiz Eduardo/Documents/Python/chromedriver")

flt_od = 'CGHSDU' #origem_destino
flt_date  = str(date.today() + timedelta(days=int(14))) #Dias de Antecedencia do voo / data_ida

decolar = 'https://www.decolar.com/shop/flights/results/oneway/'+ flt_od[:3].upper()+'/'+flt_od[-3:].upper()+'/'+flt_date+'/1/0/0/NA/NA/NA/NA/?from=SB&di=1-0'


decolar = ['https://www.decolar.com/shop/flights/results/oneway/' + b[:3].upper()+'/'+b[-3:].upper()+'/'+str(a)+'/1/0/0/NA/NA/NA/NA/?from=SB&di=1-0']
for c in decolar:
#----------------------------------Abre a página, maximiza para capturar o máximo de voos possível assim como simulua a atitude de humanos e captura o HTML----------------------------------#

    driver.get(c)
    time.sleep(6)
    driver.execute_script("window.scrollTo(0, 120000)")
    #driver.maximize_window()
    time.sleep(6)
    driver.execute_script("window.scrollTo(0, 0)")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
#--------------------------------------------------------Captura os dados iniciais do voo e quantidade de containers de voos--------------------------------------------------------#

    date_flt = soup.find("span", {"class":"route-info-item-date lowercase"})
    dep_airport = soup.find("span", {"class": "route-location route-departure-location"})
    arv_airport = soup.find("span", {"class": "route-location route-arrival-location"})
    container = soup.findAll("div", {"class": "cluster-container COMMON"})
#--------------------------------------------------------Captura os dados finais dos voos--------------------------------------------------------#

    for y in range(len(container)):
        airliners = container[y].find("span", {"class": "name"})
        dep_hour = container[y].findAll("itinerary-element", {"class": "leave"})
        arv_hour = container[y].findAll("itinerary-element", {"class": "arrive"})
        stops = container[y].findAll("span", {"data-sfa-id":"stops-text"})
        find_all_bags = container[y].findAll("span", {"class":"baggages-icons"})[0]
        Bagagem = (find_all_bags.select('span[class*="bag-image baggage-icon"]')[1])['class'][2]
        price = container[y].find("span", {"class":"fare main-fare-big"}).get_text()
        for z in range(len(dep_hour)):
            Site2 = 'Decolar'
            Data_voo = str(a)
            Cia = airliners.get_text().replace(" ", "")
            Origem = dep_airport.get_text()[1:4]
            Destino = arv_airport.get_text()[1:4]
            Tarifa = price[2:].replace(".","")
            Decolagem = dep_hour[z].get_text()
            Pouso = (arv_hour[z].get_text())[:5]
            Paradas = (stops[z].get_text()).strip()
            if (Bagagem) == 'NOT-INCLUDED':
                Bagagem = "Sem bagagem"
            elif (Bagagem) == '-INCLUDED':
                Bagagem = "Com bagagem"
#--------------------------------------------------------Imprime e registra no arquivo os dados--------------------------------------------------------#
        
            print([Data_voo+Cia+Origem+Destino+Decolagem+Pouso+Paradas+Bagagem,Site2,Data_voo,Cia,Origem+Destino,Decolagem,Pouso,Paradas,Tarifa,Bagagem])


driver.close()
