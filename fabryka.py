
import requests
import json
import csv
from datetime import date

api_url = 'https://api.czycytryny.pl/list/alerts'
secret_url = 'https://secret.czycytryny.pl/people/'
secret_token = 'yhJa8eb1jR8dqGQxixnji3g4pBs1leyH2hQvvVUC'

t = date.today()
today = t.strftime("%Y-%m-%d")
filename = "alerts-"+str(today)+".csv"

api_headers = {
    'Accept':'application/json',
    'Content-Type': 'application/json'
}

secret_headers = {
    'Accept':'application/json',
    'Content-Type': 'application/json',
    'x-api-key': secret_token
}

response = requests.request("GET",api_url,headers=api_headers,data={})
filejson = response.json()


ourdata = []
csvheader = ['event_id','type','subject','start_date','end_date','affected_personel','note']

temp_id = 0

for x in filejson:
    temp_id = 0
    listing = [x['id'],x['type'],x['subject'],x['start_date'],x['end_date'],x['affected_personel']]
    for y in x['affected_personel']:
        person_url = secret_url + y
        response = requests.request("GET", person_url, headers=secret_headers)
        filejson2 = response.text
        z = json.loads(filejson2)
        
        if response.text != "\"Not found\"":
            name=z['name'] + " " + z['surename']
            x['affected_personel'][temp_id] = z['name'] + " " + z['surename']
        else:
            name = "Nieznajomy"
            x['affected_personel'][temp_id] = "Nieznajomy"

        temp_id+=1

    ourdata.append(listing)

with open(filename,'w',encoding='UTF8',newline='') as f:
    writer = csv.writer(f)
    writer.writerow(csvheader)
    writer.writerows(ourdata)

