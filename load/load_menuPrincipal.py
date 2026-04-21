from PyQt5 import QtWidgets, uic
from load.load_ventana_psp1 import VentanaCalculadoraSum
from load.load_ventana_psp2 import VentanaCalculadoraSum2


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

