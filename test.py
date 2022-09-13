import pandas as pd
import json

csv = pd.read_csv("./data.csv", keep_default_na=False, encoding='Latin-1')
df = pd.DataFrame(csv)

data = {}
# Product Line - 10, Territory - 21, Shipped Units - 6, Net Shipped Units, Net Sales

for row in df.iterrows():
    item = row[1]
    key = str(item[10])+"+"+str(item[21])
    if(key in data):
        shippedUnits = data[key][2]
        netShippedUnits = data[key][3]
        netSales = data[key][4]
        if(item[6]=="Shipped"):
            shippedUnits = shippedUnits+1
            netSales = netSales+1
        if(item[6]=="In Process"):
            netSales = netSales+1
            netShippedUnits += 1
        if(item[6]=="Disputed"):
            netSales = netSales-1
        data[key] = [item[10], item[21], shippedUnits, netShippedUnits, netSales]

    else:
        shippedUnits = 0
        netShippedUnits = 0
        netSales = 0
        if(item[6]=="Shipped"):
            shippedUnits = 1
            netSales = 1
        if(item[6]=="In Process"):
            netSales = 1
        if(item[6]=="Disputed"):
            netSales = 0
        data[key] = [item[10], item[21], shippedUnits, netShippedUnits, netSales]

print(json.dumps(data, indent=4))

writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
data = pd.DataFrame(data).transpose()
data.columns =['Product Line', 'Territory', 'Shipped Units', 'Net Shipped Units', 'Net Sales']
data.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()