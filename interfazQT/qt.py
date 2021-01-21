from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import claseGraficador
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.grafica = claseGraficador.graficador()

        self.tipoGrafico = ''
        self.cantEmpresas = 0
        self.nombreEmpresas = []
        self.fecha = '1d'
        self.intervalo = '1d'

        self.originalPalette = QApplication.palette()
        self.createTipoGrafico()
        self.createCantEmpresas()
        self.createNombreEmpresas(self.grafica.getCantMinimaEmpresas())
        self.createFecha()
        self.createIntervalo()
        self.createGrafico()

        self.crearEstructura()
        
        self.setWindowTitle("Styles")

    def crearEstructura(self):
        layout = QGridLayout()
        layout.addWidget(self.widgetTipoGrafico,1,1)
        layout.addWidget(self.widgetCantEmpresas,1,2)
        layout.addWidget(self.widgetNombreEmpresas,1,3)
        layout.addWidget(self.fechaWidget,1,4)
        layout.addWidget(self.intervaloWidget,1,5)
        layout.addWidget(self.widgetGrafico,2,1,4,5)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)


    def createTipoGrafico(self):
        self.widgetTipoGrafico= QGroupBox("Tipo de gráfico")

        accion = QRadioButton("Graficar Acciones")
        accion.grafico = 'acciones'
        derivada = QRadioButton("Graficar Derivada")
        derivada.grafico = 'derivada'
        accion.toggled.connect(self.radioButtonToggle)
        derivada.toggled.connect(self.radioButtonToggle)
        accion.setChecked(True)
        accion.toggle()

        layout = QVBoxLayout()
        layout.addWidget(accion)
        layout.addWidget(derivada)
        self.widgetTipoGrafico.setLayout(layout)    

    def radioButtonToggle(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.tipoGrafico = radioButton.grafico

    def createCantEmpresas(self):
        self.widgetCantEmpresas = QGroupBox("Cantidad Empresas")
        comboBoxCant = QComboBox()
        for x in range(2,5):
            comboBoxCant.addItem(str(x))
        comboBoxCant.activated[str].connect(self.cambiarCantEmpresas)
        layout = QVBoxLayout()
        layout.addWidget(comboBoxCant)
        self.widgetCantEmpresas.setLayout(layout)
        
    def cambiarCantEmpresas(self,cant):
        self.cantEmpresas = int(cant)
        for w in range(len(self.widgetEmpresas)):
            if w<int(cant):
                self.widgetEmpresas[w].show()
            else:
                self.widgetEmpresas[w].hide()
        self.actualizarNombresEmpresas()

    def createNombreEmpresas(self,n):
        self.widgetNombreEmpresas = QGroupBox("Nombre de las empresas")
        self.widgetEmpresas = []
        layout = QVBoxLayout()
        listaNombres = [*self.grafica.getEmpresas()]
        c=0
        for x in range(self.grafica.getCantMaximaEmpresas()):
            comboBoxNombres = QComboBox()
            comboBoxNombres.addItems(listaNombres)
            comboBoxNombres.activated[str].connect(self.actualizarNombresEmpresas)
            layout.addWidget(comboBoxNombres)
            comboBoxNombres.setCurrentIndex(c)
            c+=1
            self.widgetEmpresas.append(comboBoxNombres)
            if x>=self.grafica.getCantMinimaEmpresas():
                comboBoxNombres.hide()
            else:
                self.nombreEmpresas.append(self.grafica.getEmpresas()[str(comboBoxNombres.currentText())])
        self.widgetNombreEmpresas.setLayout(layout)

    def actualizarNombresEmpresas(self):
        self.nombreEmpresas=[]
        for w in self.widgetEmpresas:
            if (w.isVisible()) & (self.grafica.getEmpresas()[str(w.currentText())] not in self.nombreEmpresas):
                self.nombreEmpresas.append(self.grafica.getEmpresas()[str(w.currentText())])


    def createFecha(self):
        self.fechaWidget = QGroupBox("Seleccionar Fecha")
        comboBoxFecha = QComboBox()
        comboBoxFecha.addItems(self.grafica.getFechas().keys())
        comboBoxFecha.activated[str].connect(self.actualizarFecha)
        layout = QVBoxLayout()
        layout.addWidget(comboBoxFecha)
        self.fechaWidget.setLayout(layout)

    def actualizarFecha(self,n):
        self.fecha=self.grafica.getFechas()[str(n)]
        self.createIntervalo()
        self.crearEstructura()

    def createIntervalo(self):
        self.intervaloWidget = QGroupBox("Seleccionar Intervalo")
        comboBoxIntervalo = QComboBox()
        comboBoxIntervalo.addItems(self.grafica.getIntervaloConFechas()[self.fecha])
        comboBoxIntervalo.activated[str].connect(self.actualizarIntervalo)
        layout = QVBoxLayout()
        layout.addWidget(comboBoxIntervalo)
        self.intervaloWidget.setLayout(layout)
        self.intervalo = self.grafica.getOpcionesIntervalo()[str(comboBoxIntervalo.currentText())]

    def actualizarIntervalo(self,text):
        self.intervalo=self.grafica.getOpcionesIntervalo()[str(text)]

    def createGrafico(self):
        self.widgetGrafico = QGroupBox("Gráfico")
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        button = QPushButton('Plot')
        button.clicked.connect(self.plot)
        
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(button)

        self.widgetGrafico.setLayout(layout)

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        if len(self.nombreEmpresas)<2:
            self.lanzarError('Error, se necesitan seleccionar por lo menos 2 empresas distintas.','Una sola empresa elegida')
        else:            
            self.grafica.dicGraficar[self.tipoGrafico](self.nombreEmpresas,self.fecha,self.intervalo,ax) 
            self.canvas.draw()

    def lanzarError(self,mensaje,nombre):
        dialog = QMessageBox()
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setModal(True)
        dialog.setIcon(QMessageBox.Warning)
        dialog.setText(mensaje)
        dialog.setWindowTitle(nombre)
        dialog.exec_()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
