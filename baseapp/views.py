from django.shortcuts import render
import pandas as pd
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, "home.html")

def analyze(filename):
    filename = filename[:-4]
    csv = pd.read_csv(f"./media/{filename}.csv", keep_default_na=False, encoding='Latin-1')
    df = pd.DataFrame(csv)
    data = {}
    for row in df.iterrows():
        item = row[1]
        key = str(item[10])+"+"+str(item[21])
        if(key in data):
            shippedUnits = data[key][2]
            netShippedUnits = data[key][3]
            netSales = data[key][4]
            if(item[6]=="Shipped"):
                shippedUnits = shippedUnits+1
                netShippedUnits += 1
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

    writer = pd.ExcelWriter(f'./media/{filename}.xlsx', engine='xlsxwriter')
    data = pd.DataFrame(data).transpose()
    data.columns =['Product Line', 'Territory', 'Shipped Units', 'Net Shipped Units', 'Net Sales']
    data.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    return [filename, data.values.tolist()]


def results(request):
    if request.method == "POST":
        csv = request.FILES["csvfile"]
        if csv.name.endswith('.csv'):
            fs = FileSystemStorage()
            filename = fs.save(csv.name, csv)
            receivedData = analyze(filename)
            con = {"filename": receivedData[0], "data": receivedData[1]}
            return render(request, 'results.html', context=con)
        else:
            return render(request, "error.html")