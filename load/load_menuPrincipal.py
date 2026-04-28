from PyQt5 import QtWidgets, uic
from load.load_ventana_psp1 import VentanaCalculadoraSum
from load.load_ventana_psp2 import VentanaCalculadoraSum2
from load.load_ventana_psp3 import VentanaPSP3
from load.load_ventana_psp4 import VentanaPSP4


class MenuPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
   
        uic.loadUi("gui/ventana_menu.ui", self)
        self.showMaximized()
        
       
        self.actioncalculadora.triggered.connect(self.ingresarCalculadoraSum)
        
        try:
            self.actioncalculadora_psp_2.triggered.connect(self.ingresarCalculadoraSum2)
        except Exception:
            pass
        try:
            self.actioncalculadora_psp_3.triggered.connect(self.ingresarCalculadoraSum3)
        except Exception:
            pass
        try:
            self.actioncalculadora_psp_4.triggered.connect(self.ingresarCalculadoraSum4)
        except Exception:
            pass
        self.actionsalir.triggered.connect(self.salir)

    def ingresarCalculadoraSum(self):
        self.vc = VentanaCalculadoraSum()
        self.vc.show()

    def ingresarCalculadoraSum2(self):
        
        try:
            self.vc2 = VentanaCalculadoraSum2()
            self.vc2.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo abrir el ejercicio 2: {e}")

    def salir(self):
        self.close()

    def ingresarCalculadoraSum3(self):
        try:
            self.vc3 = VentanaPSP3()
            self.vc3.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo abrir el ejercicio 3: {e}")

    def ingresarCalculadoraSum4(self):
        try:
            self.vc4 = VentanaPSP4()
            self.vc4.show()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"No se pudo abrir el ejercicio 4: {e}")

