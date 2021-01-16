from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        self.createTopLeftGroupBox()
        
        self.setCentralWidget(self.topLeftGroupBox)
        self.setWindowTitle("Styles")


    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Tipo de gráfico")

        accion = QRadioButton("Graficar Acciones")
        derivada = QRadioButton("Graficar Derivada")
        derivada.setChecked(True)


        layout = QVBoxLayout()
        layout.addWidget(accion)
        layout.addWidget(derivada)
        self.topLeftGroupBox.setLayout(layout)    

    def createComboBox(self):
        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

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
