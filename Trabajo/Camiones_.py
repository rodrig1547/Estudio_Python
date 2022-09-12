import requests
import json
import pandas as pd
from datetime import datetime

file = open('Trabajo\creds.json')
creds = json.load(file)
file.close()
df = pd.read_csv("prueba2.csv")
date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get(faena, endpoint):
    # Funcion Que recibe el nombre del endpoint y 
    # el nombre de una Faena como [LB_PROD,PETROSEA_SMD_PROD, PETROSEA_SMB_PRO, MLP_PROD]
    response = requests.request(
                                "GET",
                                 creds[faena]['url'+'_'+str(endpoint)],
                                 headers= creds[faena]['headers'], 
                                 data=creds[faena]['payload']
                                 )
    return json.loads(response.text)

def Trucks_Info(get_Trucks_Info_raw,Faena):
    ## Funcion que recibe el resultado de una consulta al endpoint y retorna la cantidad de camiones Operativos y con otros estados  
    Dict = {}
    Camiones_otro_estado = 0
    Camiones_operativos = 0
    Camiones_estado_None = 0
    for x in get_Trucks_Info_raw:
        if x['last_known_state'] is None:
            Camiones_estado_None= Camiones_estado_None+1
            #if x['last_known_position'] is not None:
            #   last_known_position.append(x['last_known_position']["t"])
        elif (x['last_known_state']['state']['name'] == 'Operativo') or (x['last_known_state']['state']['name'] == 'Efectivo') or (x['last_known_state']['state']['name'] == 'RHL (Ready Hauling)'):
            Camiones_operativos = Camiones_operativos + 1
            #if x['last_known_position'] is not None:
            #    last_known_position.append(x['last_known_position']["t"])
        elif x['last_known_state']['state']['name'] != 'Operativo':
            Camiones_otro_estado= Camiones_otro_estado+1
            #if x['last_known_position'] is not None:
            #    last_known_position.append(x['last_known_position']["t"])
    Dict['Hora_Consulta'] = date
    Dict['Faena'] = Faena
    Dict['Camiones_operativos'] = Camiones_operativos
    Dict['Camiones_otro_estado'] = Camiones_otro_estado
    Dict['Camiones_estado_None'] = Camiones_estado_None
    Dict['Camiones_totales'] = Camiones_estado_None + Camiones_otro_estado + Camiones_operativos
    #Dict['last_known_position'] = last_known_position
    
    return Dict


def Shovels_Info(get_Shovels_Info_raw, faena):
    ## Funcion que recibe el resultado de una consulta al endpoint y retorna la cantidad de Palas Operativas y otros estados
    Lista = []
    for x in get_Shovels_Info_raw:
        Dict = {}
        Dict['Hora_Consulta'] = date
        Dict['Faena'] = faena
        Dict['name_shovel'] = x['name']
        Dict['last_known_position'] = x['last_known_position']['t'] if x['last_known_position'] is not None else None 
        Dict['last_known_state'] = x['last_known_state']['state']['name'] if x['last_known_state'] is not None else None
        
        Lista.append(Dict)
    df = pd.DataFrame.from_records(Lista)     
    df.to_csv('Shovels_Status.csv', index = False, mode = 'a', header= False)
    return  True

def System_status(get_System_status,faena):
    Lista = []
    for x in get_System_status:
        Dict = {}
        Dict['Hora_Consulta'] = date
        Dict['Ultima_Actualizacion'] = x['_lastUpdated']
        Dict['Topografia'] = datetime.strptime(x['_lastUpdatedByType']['_updatedOn'], "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours = 3)
        
    

def Visualizador(hora, dict):
    Lista = {
             'Hora': [hora],
             "Camiones_operativos" : dict["Camiones_operativos"],
             "Camiones_otro_estado": dict["Camiones_otro_estado"],
             "Faena" : dict["faena"],
             "last_known_position" : dict['last_known_position'][-1]
             }
    df = pd.DataFrame(Lista)
    df.to_csv('prueba2.csv', index = False, mode = 'a', header= False )
        
def main():
    Faenas = ["LB_PROD","PETROSEA_SMD_PROD", "PETROSEA_SMB_PROD", "MLP_PROD"]
    a =[Trucks_Info(get(i, 'Trucks'), i ) for i in Faenas]    
    pd.DataFrame.from_records(a).to_csv('Estado_Camiones.csv', header= False, mode= 'a', index = False)
    b = [Shovels_Info(get(i,'Shovels' ),i) for i in Faenas] 
    print (b)

if __name__ == '__main__':
    main()