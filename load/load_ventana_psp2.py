from PyQt5 import QtWidgets, uic
from psp.ejercicio2.ejercicio2 import Sumasim


class VentanaCalculadoraSum2(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi("gui/ventana_psp2.ui", self)
       
        try:
            self.botoncalcular2.clicked.connect(self.calcular)
        except Exception:
            pass

    def calcular(self):
        
        try:
            x_txt = self.valorx2.text().strip()
            dof_txt = self.valordof2.text().strip()
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Error UI", "No se encontraron los campos de entrada en la UI.")
            return

        try:
            x = float(x_txt)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Introduce un número válido en X.")
            return

        try:
            dof = float(dof_txt)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Introduce un número válido en DOF.")
            return

        
        a = 0.0
        b = x
        n = 100

        try:
            s = Sumasim(a, b, n, dof)
            s.integrar()
            resultado = getattr(s, 'resultado', None)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error cálculo", f"Error al ejecutar Sumasim: {e}")
            return

        try:
           
            self.label_3.setText(str(resultado))
        except Exception:
          
            try:
                self.label_resultado.setText(str(resultado))
            except Exception:
                pass
        
