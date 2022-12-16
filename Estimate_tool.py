import pyodbc
from sklearn import preprocessing,tree

x = []
y = []

conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=DESKTOP-0A40BHV;'
                    'Database=USEDCARS;'
                    'Trusted_Connection=yes;')

cursor = conn.cursor()
query = 'SELECT Model,Price,Mileage,City FROM CarsUsed WHERE Price NOT LIKE \'%???????%\' AND Price NOT LIKE N\'%توافقی%\' AND Mileage NOT LIKE N\'%???????%\''
cursor.execute(query)

tmp1 = []
tmp2 = []

for Info in cursor: 
    tmp1.append(Info[0])   
    tmp2.append(Info[3])
    x.append([Info[2]])
    y.append(Info[1])

cursor.close()
conn.close()

le = preprocessing.LabelEncoder()
le.fit(tmp1)
list(le.classes_)
tmp1 = le.transform(tmp1)

le = preprocessing.LabelEncoder()
le.fit(tmp2)
list(le.classes_)
tmp2 = le.transform(tmp2)

for this_one in range(len(tmp1)):
    x[this_one].append(tmp1[this_one])
    x[this_one].append(tmp2[this_one])


clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)

your_used_cars = input().split()

tmp = [your_used_cars[1], your_used_cars[2]]

le = preprocessing.LabelEncoder()
le.fit(tmp)
list(le.classes_)
tmp = le.transform(tmp)

price = clf.predict([[your_used_cars[0],tmp[0],tmp[1]]])
print(price)