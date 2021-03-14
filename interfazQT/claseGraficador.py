import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as dates


class graficador():
    
    def __init__(self):
        self.cantLimiteEmpresas=(2,5)
        self.listaFechas={'dia anterior':'1d','5 dias':'5d','1 mes':'1mo','3 meses':'3mo','6 meses':'6mo','1 año':'1y',
        '2 años':'2y','5 años':'5y','10 años':'10y','historia completa':'max'}
        self.intervaloConFechas={
            '1d':['30 minutos', '1 Hora'],
            '5d':['30 minutos','1 Hora','1 dia'],
            '1wk':['1 Hora','1 dia','5 dias'],
            '1mo':['1 dia','5 dias','1 semana'],
            '3mo':['1 dia','5 dias','1 semana','1 mes'],
            '6mo':['1 dia','5 dias','1 semana','1 mes','3 meses'],
            '1y':['1 dia','1 semana','1 mes','3 meses'],
            '2y':['1 dia','1 semana','1 mes','3 meses'],
            '5y':['1 dia','1 semana','1 mes','3 meses'],
            '10y':['1 dia','1 semana','1 mes','3 meses'],
            'max':['1 dia','1 semana','1 mes','3 meses']
        }
        self.opcionesIntervalo={'1 minuto':'1m','5 minutos':'5m','15 minutos':'15m','30 minutos':'30m','1 Hora':'60m'
        ,'1 dia':'1d','5 dias':'5d','1 semana':'1wk','1 mes':'1mo','3 meses':'3mo'}
        self.empresas={'Amazon':'AMZN','Microsoft':'MSFT','Apple':'AAPL','Tesla':'TSLA','Johnson & Johnson':'JNJ','Google':'GOOGL',
        'Nvidia':'NVDA','JP Morgan':'JPM','Netflix':'NFLX','Coca cola':'KO','Pfizer':'PFE','Banco Santander Rio':'BRIO'}
        self.nombreGrafico='grafico'
        self.nombreCSV='salida'
        self.dicGraficar = {'acciones':self.graficoAccionesFuncionTiempo,'derivada':self.graficoDerivada}


    def getIntervaloConFechas(self):
        return self.intervaloConFechas

    def getEmpresas(self):
        return self.empresas

    def getOpcionesIntervalo(self):
        return self.opcionesIntervalo

    def getCantMinimaEmpresas(self):
        return self.cantLimiteEmpresas[0]

    def getCantMaximaEmpresas(self):
        return self.cantLimiteEmpresas[1]

    def getFechas(self):
        return self.listaFechas


    def graficoAccionesFuncionTiempo(self,nombreEmpresas,fecha,intervalo,ax):
        data = yf.download(tickers=nombreEmpresas,interval=intervalo,period=fecha)
        data = data['Close']
        data = data.reset_index()
        data.dropna(axis=0,inplace=True)
        if intervalo in ['1m','5m','15m','30m','60m']:
            plt.xticks(rotation=70)
            data['Date']=data['Datetime'].apply(lambda x:str(x.day)+','+str(x.hour)+':'+str(x.minute))
        listaDatos=[]
        for accion in nombreEmpresas:
            ax.plot('Date',accion,data=data,linewidth=2)
            listaDatos.append([data[accion].to_numpy(),accion])
        x=data['Date'].to_numpy()
        accionesYaGraficadas=[]
        idxl=[]
        for lista in listaDatos:
            for lista2 in listaDatos:
                if (lista[1]==lista2[1]) | (lista[1] in accionesYaGraficadas) & (lista2[1] in accionesYaGraficadas):
                    continue
                idx = np.argwhere(np.diff(np.sign(lista[0] - lista2[0]))).flatten()
                ax.plot(x[idx], lista[0][idx], 'ro')
                idxl.extend(idx)
            accionesYaGraficadas.append(lista[1])
        exportarAcsv(listaDatos,x,idxl,self.nombreCSV+'.csv')
        ax.set_xlabel('FECHA', fontsize=20)
        ax.set_ylabel('VALOR', fontsize=20)
        ax.grid()
        ax.legend()
    

    def graficoDerivada(self,nombreEmpresas,fecha,intervalo,ax):
        data = yf.download(tickers=nombreEmpresas,interval=intervalo,period=fecha)
        data = data['Close']
        data = data.reset_index()
        data.dropna(axis=0,inplace=True)
        if intervalo in ['1m','5m','15m','30m','60m']:
            plt.xticks(rotation=70)
            data['Date']=data['Datetime'].apply(lambda x:str(x.day)+','+str(x.hour)+':'+str(x.minute))
        listaAcciones=[]
        for accion in nombreEmpresas:
            listaAcciones.append([data[accion].to_numpy(),accion])  #lista[0][0]->serie numpy#lista[0][1]->nombre de la accion
        x=data['Date'].to_numpy()    
        for dato in range (1,len(listaAcciones)):
            listaAcciones[dato][0]=listaAcciones[dato][0]-listaAcciones[dato-1][0]
        for dato in range (0,len(listaAcciones)):
            ax.plot(data['Date'],listaAcciones[dato][0],label=listaAcciones[dato][1],linewidth=2)   
        accionesYaGraficadas=[] 
        idxl=[]
        for lista1 in listaAcciones:
            for lista2 in listaAcciones:  
                if (lista1[1]==lista2[1]) | (lista1[1] in accionesYaGraficadas) & (lista2[1] in accionesYaGraficadas):
                    continue
                idx = np.argwhere(np.diff(np.sign(lista1[0] - lista2[0]))).flatten()
                ax.plot(x[idx], lista1[0][idx], 'ro')
                idxl.extend(idx)
            accionesYaGraficadas.append(lista1[1])
        exportarAcsv(listaAcciones,x,idxl,self.nombreCSV+'.csv')
        ax.set_xlabel('FECHA', fontsize=20)
        ax.set_ylabel('DERIVADA', fontsize=20)
        ax.legend()


        
def exportarAcsv(listaDatos,x,idx,nombreDoc):
    f = open(nombreDoc,'w')
    f.write(';')
    for lista in listaDatos:
        f.write(lista[1]+';')
    f.write("\n")
    for j in range(len(listaDatos[0][0])):
        escrInter=False
        f.write(str(x[j])+';')
        for i in range(len(listaDatos)):
            f.write(str(np.round(listaDatos[i][0][j],2)))
            f.write(';')
            if (listaDatos[i][0][j].size>0) & (len(idx)>0):
                escrInter=(listaDatos[i][0][j] in idx)
        if escrInter:
            f.write('interseccion;')
        f.write('\n')
    f.close()
