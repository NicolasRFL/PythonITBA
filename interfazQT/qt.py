from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.createTipoGrafico()
        #self.createCantEmpresas()
        #self.createFecha()
        #self.createIntervalo()

        layout = QVBoxLayout()
        layout.addWidget(self.tipoGrafico)
        #layout.addWidget(self.cantEmpresas)
        #layout.addWidget(self.nombreEmpresas)
        #layout.addWidget(self.fecha)
        #layout.addWidget(self.intervlo)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setWindowTitle("Styles")


    def createTipoGrafico(self):
        self.tipoGrafico= QGroupBox("Tipo de gráfico")

        accion = QRadioButton("Graficar Acciones")
        derivada = QRadioButton("Graficar Derivada")
        derivada.setChecked(True)


        layout = QVBoxLayout()
        layout.addWidget(accion)
        layout.addWidget(derivada)
        self.tipoGrafico.setLayout(layout)    

    def createCantEmpresas(self):
        self.cantEmpresas = QGroupBox("Cantidad Empresas")
        comboBoxCant = QComboBox()
        comboBoxCant.addItems(QStyleFactory.keys())

        styleLabel = QLabel("Graficador acciones:")
        styleLabel.setBuddy(styleComboBox)
        styleComboBox.activated[str].connect(self.changeStyle)


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
