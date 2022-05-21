import requests
from datetime import datetime
import pandas as pd
BASE='http://127.0.0.1:5000/'

fechas = pd.date_range(end = '2021-03-10', periods=120)
contador=0
def poblarbase():
    for i in fechas:
        formatofecha= str(i).split()
        url=BASE+"put_photo/"+str(contador)+"/"+formatofecha[0]
        response=requests.put(url)
        contador=contador+1
def poblarbaseUNO(id):
        i=fechas[id]
        formatofecha= str(i).split()
        url=BASE+"put_photo/"+str(id)+"/"+formatofecha[0]
        response=requests.put(url)
def getbase(idP):
    id=str(idP)
    response=requests.get(BASE+"get_photo/"+id)
    respuesta=response.json()
    print(respuesta)
def deletebase(idP):
    id=str(idP)
    response=requests.delete(BASE+"delete_photo/"+id)
    respuesta=response.json()
    print(respuesta)
def updatebase(idP):
    id=str(idP)
    response=requests.delete(BASE+"delete_photo/"+id)
    respuesta=response.json()
    print(respuesta)
#poblarbaseUNO(1)
getbase(1)
#deletebase(1)