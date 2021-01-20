import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as dates


class graficador():
    
    def __init__(self):
        self.nombreEmpresas=[]
        self.cantEmpresas=2
        self.cantLimiteEmpresas=(2,5)
        self.tipoGrafico=''
        self.listaFechas={'dia anterior':'1d','5 dias':'5d','1 mes':'1mo','3 meses':'3mo','6 meses':'6mo','1 año':'1y','2 años':'2y',
    '5 años':'5y','10 años':'10y','historia completa':'max'}
        self.fecha=0
        self.intervalo=0
        self.opcionesIntervalo={'un dia':'1d','cinco dias':'5d','una semana':'1wk','un mes':'1mo','tres meses':'3mo'}
        self.empresas={'Amazon':'AMZN','Microsoft':'MSFT','Apple':'AAPL','Tesla':'TSLA','Johnson & Johnson':'JNJ','Google':'GOOGL',
        'Nvidia':'NVDA','JP Morgan':'JPM','Netflix':'NFLX','Coca cola':'KO','Pfizer':'PFE','Banco Santander Rio':'BRIO'}
        self.nombreGrafico='grafico'
        self.nombreCSV='salida'
        self.dicGraficar = {'acciones':self.graficoAccionesFuncionTiempo,'derivada':self.graficoDerivada}

    def setTipoGrafico(self,n):
        self.tipoGrafico = n

    def setCantEmpresas(self,n):
        self.cantEmpresas = n

    def getEmpresas(self):
        return self.empresas

    def getOpcionesIntervalo(self):
        return self.opcionesIntervalo

    def getCantEmpresas(self):
        return self.cantEmpresas

    def getCantMinimaEmpresas(self):
        return self.cantLimiteEmpresas[0]

    def getCantMaximaEmpresas(self):
        return self.cantLimiteEmpresas[1]

    def getFechas(self):
        return self.listaFechas

    def graficar(self):
        self.dicGraficar[self.tipoGrafico]()

    def graficoAccionesFuncionTiempo(self):
        data = yf.download(tickers=self.nombreEmpresas,interval=self.intervalo,period=self.fecha)
        data=data['Close']
        data.reset_index(inplace=True)
        data.dropna(axis=0,inplace=True)
        plt.figure(figsize=(16, 16))
        listaDatos=[]
        for accion in self.nombreEmpresas:
            plt.plot('Date',accion,data=data,linewidth=2)
            listaDatos.append([data[accion].to_numpy(),accion])
        x=data['Date'].to_numpy()
        accionesYaGraficadas=[]
        idxl=[]
        for lista in listaDatos:
            for lista2 in listaDatos:
                if (lista[1]==lista2[1]) | (lista[1] in accionesYaGraficadas) & (lista2[1] in accionesYaGraficadas):
                    continue
                idx = np.argwhere(np.diff(np.sign(lista[0] - lista2[0]))).flatten()
                plt.plot(x[idx], lista[0][idx], 'ro')
                idxl.extend(idx)
            accionesYaGraficadas.append(lista[1])
        exportarAcsv(listaDatos,x,idxl,self.nombreCSV+'.csv')
        plt.xlabel('FECHA', fontsize=20)
        plt.ylabel('VALOR', fontsize=20)
        plt.legend()
        plt.savefig(self.nombreCSV+'.png')
    

    def graficoDerivada(self):
        data = yf.download(tickers=self.nombreEmpresas,interval=self.intervalo,period=self.fecha)
        data=data['Close']
        data.reset_index(inplace=True)
        data.dropna(axis=0,inplace=True)
        plt.figure(figsize=(16, 16))
        listaAcciones=[]
        for accion in self.nombreEmpresas:
            listaAcciones.append([data[accion].to_numpy(),accion])  #lista[0][0]->serie numpy#lista[0][1]->nombre de la accion
        x=data['Date'].to_numpy()    
        for dato in range (1,len(listaAcciones)):
            listaAcciones[dato][0]=listaAcciones[dato][0]-listaAcciones[dato-1][0]
        for dato in range (0,len(listaAcciones)):
            plt.plot(data['Date'],listaAcciones[dato][0],label=listaAcciones[dato][1],linewidth=2)   
        accionesYaGraficadas=[] 
        idxl=[]
        for lista1 in listaAcciones:
            for lista2 in listaAcciones:  
                if (lista1[1]==lista2[1]) | (lista1[1] in accionesYaGraficadas) & (lista2[1] in accionesYaGraficadas):
                    continue
                idx = np.argwhere(np.diff(np.sign(lista1[0] - lista2[0]))).flatten()
                plt.plot(x[idx], lista1[0][idx], 'ro')
                idxl.append(idx)
            accionesYaGraficadas.append(lista1[1])
        exportarAcsv(listaAcciones,x,idxl,self.nombreCSV+'.csv')
        plt.xlabel('FECHA', fontsize=20)
        plt.ylabel('DERIVADA', fontsize=20)
        plt.legend()
        plt.savefig(self.nombreCSV+'.png')


        
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
            if (listaDatos[i][0][j].size>0) & (idx[i].size>0):
                escrInter=(listaDatos[i][0][j] in idx[i])
        if escrInter:
            f.write('interseccion;')
        f.write('\n')
    f.close()
