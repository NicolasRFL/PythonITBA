import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as dates



def main():
    imprimirBienvenida()
    y=True
    intervalo="1d"
    duracion="1y"
    cantAcciones=2
    while (y):
        modo = input('Escriba modo:')
        if (modo=='graficar') | (modo=='g'):
            lista,tipo=recibirInputs(cantAcciones)    
            y=graficar(lista,tipo,intervalo,duracion)
        elif (modo=='cantidad') | (modo=='c'):
            cantAcciones=modificarCantAcciones()
        elif (modo=='intervalo') | (modo=='i'):
            intervalo=modificarIntervaloDeTiempo()
        elif (modo=='fecha') | (modo=='f'):
            duracion=modificarFechaInicio()
        elif (modo=='ayuda') |( modo=='a'):
            mostrarAyuda()
        elif (modo=='salir') | (modo=='s'):
            return 0
    return 0

def graficar(lista,tipo,intervalo,duracion):
    if (tipo=='grafico 1') | (tipo=='1'):
        graficoAccionesFuncionTiempo(lista,intervalo,duracion)
    else:
        graficoDerivada(lista,intervalo,duracion)
    return preguntarContinuar()

def preguntarContinuar():
    print ("Grafico terminado!")
    print ("Puede crear otro grafico o salir de la aplicacion")
    print ("Escriba nuevo o n para crear un nuevo grafico")
    print ("Escriba cualquier otra cosa para salir")
    x = input("¿Salir o nuevo?: ")
    if (x=='nuevo') |( x=='n'):
        return True
    return False

def imprimirBienvenida():
    print ("""Este programa permite graficar los valores de cierre en funcion de tiempo o la derivada de 
    estos valores para las acciones de una empresa""")
    print ("Para usar este programa se debe ingresar comandos a medida que se van pidiendo.")
    print ("Escriba ayuda o a para mostrar que comandos existen")


def mostrarAyuda():
    print ("Los comandos validos son:")
    print ("""Para hacer un grafico donde solo se especifican 2 empresas y que tipo de grafico se desea hacer, escriba:""")
    print ("g o grafico")
    print ("Para modificar la cantidad de empresas que se van a graficar escriba:")
    print ("c o cantidad")
    print ("Para modificar el intervalo de tiempo que se va a graficar escriba:")
    print ("i o intervalo")
    print ("Para modificar la fecha desde la cual se va a graficar hasta el dia de hoy, escriba:")
    print ("f o fecha")
    print ("""Para mostrar un menú de ayuda escriba con estos comandos escriba: """)
    print ("a o ayuda")
    print ("""Para cerrar este programa escriba:""")
    print ("s o salida")


def mostrarError(listaOpciones):
    print ("Opcion no valida!")
    print ("Las opciones son: ")
    print (listaOpciones)

def recibirInputs(cantEmpresas):
    esperandoInput=True
    empresas={'Amazon':'AMZN','Microsoft':'MSFT','Apple':'AAPL','Tesla':'TSLA','Johnson & Johnson':'JNJ','Google':'GOOGL',
    'Nvidia':'NVDA','JP Morgan':'JPM','Netflix':'NFLX','Coca cola':'KO','Pfizer':'PFE','Banco Santander Rio':'BRIO'}
    print ("Lista de empresas disponibles: \n")
    listaEmpresas=[*empresas]
    print (",".join(listaEmpresas))
    listaObjetivos=obtenerObjetivos(listaEmpresas,cantEmpresas)
    listaObjetivos=[empresas.get(l) for l in listaObjetivos]
    print ("¿Que desea graficar?")
    print ("Para graficar el valor de las acciones en funcion del tiempo escriba: \ngrafico 1")
    print ("Para graficar la derivada discreta de las acciones en funcion del tiempo escriba:\ngrafico 2")
    while (esperandoInput):
        tipoGrafico=input("Escriba:")
        if ((tipoGrafico=='1') | (tipoGrafico.lower()=='grafico 1') | (tipoGrafico=='2') | (tipoGrafico.lower()=='grafico 2')):
            esperandoInput = False
        else:
            mostrarError(['grafico 1','1','grafico 2','2'])
    return listaObjetivos,tipoGrafico


def modificarCantAcciones():
    esperandoInput=True
    print ('¿Cuantas empresas quiere obtener informacion? El limite minimo es 1 y el maximo es 6')
    while esperandoInput:
        cantEmpresas=input('Ingrese un numero')
        if not cantEmpresas.isdigit():
            print ("Error ingrese un numero sin letras")
        elif not ((cantEmpresas<=6) & (cantEmpresas>=1)):
            print ("Error ingrese un numero mayor o igual a 1 y menor o igual a 6")
        else:
            esperandoInput=False
    return  int(cantEmpresas)

def modificarIntervaloDeTiempo():
    esperandoInput=True
    print ("¿Que intervalo de tiempo le gustaria usar en el grafico?")
    print ("Las opciones son:")
    opcionesIntervalo={'un dia':'1d','cinco dias':'5d','una semana':'1wk','un mes':'1mo','tres meses':'3mo'}
    print ([*opcionesIntervalo])
    while (esperandoInput):
        intervalo=input('Esperando input: ')
        if intervalo in [*opcionesIntervalo]:
            esperandoInput=False
        else:
            mostrarError([*opcionesIntervalo])
    intervalo=opcionesIntervalo.get(intervalo)
    return intervalo

def modificarFechaInicio():
    esperandoInput=True    
    print ("Se puede elegir desde que fecha se empiezan a tomar en cuenta las acciones, respecto el dia de hoy")
    print ("¿Desde que fecha quiere que comienze el grafico?")
    opcionesFecha={'dia anterior':'1d','5 dias':'5d','1 mes':'1mo','3 meses':'3mo','6 meses':'6mo','1 año':'1y','2 años':'2y',
    '5 años':'5y','10 años':'10y','historia completa':'max'}
    print ("Puede ser la fecha de hoy menos: ")
    print ([*opcionesFecha])
    while (esperandoInput):
        fechaInicio=input('Esperando input: ')
        if (fechaInicio in [*opcionesFecha]):
            esperandoInput=False
        else:
            mostrarError ([*opcionesFecha])
    fechaInicio = opcionesFecha.get(fechaInicio)
    return fechaInicio
     
def graficoAccionesFuncionTiempo(lista,intervalo,fechaInicio):
    data = yf.download(tickers=lista,interval=intervalo,period=fechaInicio)
    data=data['Close']
    data.reset_index(inplace=True)
    data.dropna(axis=0,inplace=True)
    plt.figure(figsize=(16, 16))
    listaDatos=[]
    for accion in lista:
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
    exportarAcsv(listaDatos,x,idxl,'accionesFuncTiempo.csv')
    plt.xlabel('FECHA', fontsize=20)
    plt.ylabel('VALOR', fontsize=20)
    plt.legend()
    plt.savefig('acciones.png')
        
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
                escrInter=(listaDatos[i][0][j] in idx[i])
        if escrInter:
            f.write('interseccion;')
        f.write('\n')
    f.close()


def graficoDerivada(lista,intervalo,fechaInicio):
    data = yf.download(tickers=lista,interval=intervalo,period=fechaInicio)
    data=data['Close']
    data.reset_index(inplace=True)
    data.dropna(axis=0,inplace=True)
    plt.figure(figsize=(16, 16))
    listaAcciones=[]
    for accion in lista:
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
    exportarAcsv(listaAcciones,x,idxl,"derivadaAcciones.csv")
    plt.xlabel('FECHA', fontsize=20)
    plt.ylabel('DERIVADA', fontsize=20)
    plt.legend()
    plt.savefig('derivada.png')

def obtenerObjetivos(empresas,cantEmpresas):    
    listaObjetivos=[]
    i=0
    print ("Se pueden graficar hasta "+ str(cantEmpresas) + " empresas")
    while (i<cantEmpresas):
        empresa = input("Escribi el nombre de la empresa cuyas acciones quieras graficar: ")
        if (empresa not in empresas):
            mostrarError([*empresas])
        elif (empresa in listaObjetivos):
            print ("Nombre repetido")
        else:
            listaObjetivos.append(empresa)
            i+=1
            print ("Hasta ahora se van a graficar: "+(",").join(listaObjetivos))
    return listaObjetivos


main()