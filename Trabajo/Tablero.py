import requests

url = "https://timineaware-lb.azurefd.net/assets/remote-document/query/raw_trucks_trucks"

payload={}
headers = {
  'x-api-key': '83fc13c9-8c65-4773-8000-675f72c579cf'
}

response = requests.request("GET", url, headers=headers, data=payload)

def Estado_Camiones(response):
    table = response
    return table

#print (response.text)
for i in response:
    print (i)
    print ('------')