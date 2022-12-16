from requests import get
from bs4 import BeautifulSoup
import re
import pyodbc

def toint(num:str):
    if 'توافقی'  in num:
        return num

    number = ''
    num = re.findall('\d*',num)

    for this_one in num:
        if this_one != None:
            number += str(this_one)

    return number

base_url = 'https://bama.ir/car'
response = get(base_url)
html_soup = BeautifulSoup(response.text, 'html.parser')

cars_in_cuurent_page = html_soup.find_all('div' , attrs={'class' : 'title'})


cars = list()

for page in range(8):
    cars_data_ids = html_soup.find_all(attrs={"data-id": True})
    cars_ids = list()
    for id in cars_data_ids:
        cars_ids.append(id['data-id'])
    
    id_index = 0
    for car in cars_in_cuurent_page:
        url = car.find(href=True)['href']
        res = get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
    
        id = cars_ids[id_index]
        car_Model = soup.find('h1', attrs = {'class':'addetail-title'}).find_all('span')
        index_Model = 0
        Model = ''
        
        for this_one in car_Model:
            if index_Model == 0 or index_Model == 3:
                Model += this_one.text.strip() + ' '
    
        car_infos = soup.find('div', attrs = {'class':'inforight'}).find_all('p')
        car_infos_index = 0                
        Price = car_infos[0].text.strip().split()[1]        
        Mileage = car_infos[2].text.strip().split()[1]        
        City = ' '
        for item in car_infos[9].text.strip().split():
            City += str(item) + ' '
        
        cars.append({'Id' : id ,'Model' : Model 
        ,'Price' : toint(Price) ,'Mileage' : toint(Mileage) ,'City' : City})
        id_index += 1
    
    url = html_soup.find('div' , attrs={'class' : 'car-ad-list next'}).find(href=True)['href']




conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-0A40BHV;'
                    'Database=USEDCARS;'
                    'Trusted_Connection=yes;')
    
cursor = conn.cursor()
for car in cars:
    add_car = 'INSERT INTO TempCars (Id, Model, Price, Mileage, City) VALUES (\'{}\',N\'{}\',N\'{}\',\'{}\',N\'{}\')'.format(
        car['Id'],car['Model'],car['Price'],'نامعلوم' if car['Mileage'] == '' else car['Mileage'],car['City']
        )

    cursor.execute(add_car)    
    conn.commit()

query = '''INSERT INTO CarsUsed
	(Id, Model, Price, Mileage, City)
	SELECT DISTINCT t1.Id, t1.Model, t1.Price, t1.Mileage, t1.City           
    FROM TempCars t1
	WHERE t1.Id NOT IN (SELECT Id
	FROM CarsUsed)'''

cursor.execute(query)    
conn.commit()

cursor.close()
conn.close()