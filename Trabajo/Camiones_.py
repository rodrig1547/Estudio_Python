import requests
import json
import pandas as pd
from datetime import datetime

file = open('creds.json')
creds = json.load(file)
file.close()
df = pd.read_csv("prueba2.csv")
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get(endpoint, faena):
    # Funcion Que recibe el nombre del endpoint y 
    # el nombre de una Faena como [LB_PROD,PETROSEA_SMD_PROD, PETROSEA_SMB_PRO, MLP_PROD]
    response = requests.request(
                                "GET",
                                 creds[endpoint][faena]['url'],
                                 headers= creds[endpoint][faena]['headers'], 
                                 data=creds[endpoint][faena]['payload']
                                 )
    return json.loads(response.text)

def Trucks_Operativos(get_Trucks_Infor_raw):
    ## Funcion que recibe el resultado de una consulta al endpoint y retorna la cantidad de camiones Operativos y con otro estado  
    Camiones_otro_estado = 0
    Camiones_operativos = 0
    for x in get_Trucks_Infor_raw:
        if x['last_known_state'] is None:
            Camiones_otro_estado= Camiones_otro_estado+1
        elif x['last_known_state']['state']['name'] == 'Operativo':
            Camiones_operativos = Camiones_operativos + 1
        elif x['last_known_state']['state']['name'] != 'Operativo':
            Camiones_otro_estado= Camiones_otro_estado+1
    return Camiones_operativos, Camiones_otro_estado

def Visualizador(hora, faena, Camiones_operativos, Camiones_otro_estado):
    Lista = {'Hora': [hora],
             "Camiones_operativos" : [Camiones_operativos],
             "Camiones_otro_estado": [Camiones_otro_estado],
             "Faena" : [faena]}
    df = pd.DataFrame(Lista)
    df.to_csv('prueba2.csv', index = False, mode = 'a', header= False )

        

def shovel(x):
    dict1 = {}
    for i in x:
        print (i)
        a = i['last_known_position']
        b = i['last_known_state']
        dict1[i['name']] = {'last_known_position' : i['last_known_position']['t'] if a!=None else None, 'last_known_state' : i['last_known_state']['state']['name'] if a!=None else None}
    return dict1
    
def main():
    a = Trucks_Operativos(get('Truck','LB_PROD'))
    print (a[0], a[1])
    print (date)
    Visualizador(date,'LB_PROD',a[0],a[1])

if __name__ == '__main__':
    main()