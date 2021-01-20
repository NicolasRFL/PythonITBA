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

        self.originalPalette = QApplication.palette()
        self.createTipoGrafico()
        self.createCantEmpresas()
        self.createNombreEmpresas(self.grafica.getCantMinimaEmpresas())
        self.createFecha()
        self.createIntervalo()
        self.createGrafico()

        self.tipoGrafico = ''
        self.cantEmpresas = 0
        self.nombreEmpresas = []
        self.fecha = '1d'
        self.intervalo = '1d'

        layout = QGridLayout()
        layout.addWidget(self.widgetTipoGrafico,1,1)
        layout.addWidget(self.widgetCantEmpresas,1,2)
        layout.addWidget(self.widgetNombreEmpresas,1,3)
        layout.addWidget(self.fechaWidget,1,4)
        layout.addWidget(self.intervaloWidget,1,5)
        layout.addWidget(self.grafico,2,1,4,5)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setWindowTitle("Styles")


    def createTipoGrafico(self):
        self.widgetTipoGrafico= QGroupBox("Tipo de gráfico")

        accion = QRadioButton("Graficar Acciones")
        accion.grafico = 'acciones'
        derivada = QRadioButton("Graficar Derivada")
        derivada.grafico = 'derivada'
        accion.toggled.connect(self.radioButtonToggle)
        derivada.toggled.connect(self.radioButtonToggle)
        accion.setChecked(True)


        layout = QVBoxLayout()
        layout.addWidget(accion)
        layout.addWidget(derivada)
        self.widgetTipoGrafico.setLayout(layout)    

    def radioButtonToggle(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.grafica.setTipoGrafico(radioButton.grafico)

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
        for x in range(self.grafica.getCantMaximaEmpresas()):
            comboBoxNombres = QComboBox()
            comboBoxNombres.addItems(listaNombres)
            comboBoxNombres.activated[str].connect(self.actualizarNombresEmpresas)
            layout.addWidget(comboBoxNombres)
            if x>=self.grafica.getCantMinimaEmpresas():
                comboBoxNombres.hide()
            self.widgetEmpresas.append(comboBoxNombres)
        self.widgetNombreEmpresas.setLayout(layout)

    def actualizarNombresEmpresas(self):
        self.nombreEmpresas=[]
        for w in self.widgetEmpresas:
            if w.isVisible():
                self.nombreEmpresas.append(str(w.currentText()))

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

    def createIntervalo(self):
        self.intervaloWidget = QGroupBox("Seleccionar Intervalo")
        comboBoxIntervalo = QComboBox()
        comboBoxIntervalo.addItems(self.grafica.getOpcionesIntervalo().keys())
        comboBoxIntervalo.activated[str].connect(self.actualizarIntervalo)
        layout = QVBoxLayout()
        layout.addWidget(comboBoxIntervalo)
        self.intervaloWidget.setLayout(layout)

    def actualizarIntervalo(self,text):
        self.intervalo=self.grafica.getOpcionesIntervalo()[str(text)]

    def createGrafico(self):
        self.grafico = QGroupBox("Gráfico")
        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        toolbar = NavigationToolbar(canvas, self)

        # Just some button connected to `plot` method
        button = QPushButton('Plot')
        button.clicked.connect(self.plot)
        
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        layout.addWidget(button)

        self.grafico.setLayout(layout)

    def plot(self):
        self.tipoGrafico


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
