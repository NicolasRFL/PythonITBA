from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import claseGraficador

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.grafica = claseGraficador.graficador()

        self.originalPalette = QApplication.palette()
        self.createTipoGrafico()
        self.createCantEmpresas()
        self.createNombreEmpresas()
        self.createFecha()
        self.createIntervalo()
        self.createGrafico()

        layout = QGridLayout()
        layout.addWidget(self.tipoGrafico,1,1)
        layout.addWidget(self.cantEmpresas,1,2)
        layout.addWidget(self.nombreEmpresas,1,3)
        layout.addWidget(self.fecha,1,4)
        layout.addWidget(self.intervalo,1,5)
        layout.addWidget(self.grafico,2,1,4,5)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setWindowTitle("Styles")


    def createTipoGrafico(self):
        self.tipoGrafico= QGroupBox("Tipo de gráfico")

        accion = QRadioButton("Graficar Acciones")
        derivada = QRadioButton("Graficar Derivada")
        accion.setChecked(True)


        layout = QVBoxLayout()
        layout.addWidget(accion)
        layout.addWidget(derivada)
        self.tipoGrafico.setLayout(layout)    

    def createCantEmpresas(self):
        self.cantEmpresas = QGroupBox("Cantidad Empresas")
        comboBoxCant = QComboBox()
        for x in range(2,5):
            comboBoxCant.addItem(str(x))

        layout = QVBoxLayout()
        layout.addWidget(comboBoxCant)
        self.cantEmpresas.setLayout(layout)

        #styleLabel = QLabel("Graficador acciones:")
        #styleComboBox.activated[str].connect(self.changeStyle)

    def createNombreEmpresas(self):
        self.nombreEmpresas = QGroupBox("Nombre de las empresas")
        layout = QVBoxLayout()
        for x in range(self.grafica.getCantLimiteEmpresas()):
            comboBoxNombres = QComboBox()
            comboBoxNombres.addItems(self.grafica.getEmpresas().keys())
            if x>1:
                comboBoxNombres.hide()
            layout.addWidget(comboBoxNombres)
        self.nombreEmpresas.setLayout(layout)

        #styleLabel = QLabel("Graficador acciones:")
        #styleComboBox.activated[str].connect(self.changeStyle)

    def createFecha(self):
        self.fecha = QGroupBox("Seleccionar Fecha")
        comboBoxFecha = QComboBox()
        comboBoxFecha.addItems(self.grafica.getFechas().keys())
        layout = QVBoxLayout()
        layout.addWidget(comboBoxFecha)
        self.fecha.setLayout(layout)

    def createIntervalo(self):
        self.intervalo = QGroupBox("Seleccionar Intervalo")
        comboBoxIntervalo = QComboBox()
        comboBoxIntervalo.addItems(self.grafica.getOpcionesIntervalo().keys())

        layout = QVBoxLayout()
        layout.addWidget(comboBoxIntervalo)
        self.intervalo.setLayout(layout)

    def createGrafico(self):
        self.grafico = QGroupBox("Gráfico")
        graff = QLabel()
        pixmap = QPixmap(r'C:\Users\Nicolas\Documents\GitHub\PythonITBA\acciones.png').scaled(640, 640, Qt.KeepAspectRatio)
        graff.setPixmap(pixmap)

        layout = QVBoxLayout()
        layout.addWidget(graff)
        self.grafico.setLayout(layout)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
