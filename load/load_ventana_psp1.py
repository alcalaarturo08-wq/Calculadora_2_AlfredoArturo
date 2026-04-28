from PyQt5 import QtWidgets, uic
from psp.ejercicio1.ejercicio1 import CalculadoraSum


class VentanaCalculadoraSum(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
      

        uic.loadUi("gui/ventana_psp1.ui", self)
        self.case1_x = [130,650,99,150,128,302,95,945,368,961]
        self.case1_y = [186,699,132,272,291,331,199,1890,788,1601]


    
        self.case2_x = [130,650,99,150,128,302,95,945,368,961]
        self.case2_y = [15,69.9,6.5,22.4,28.4,65.9,19.4,198.7,38.8,138.2] 


        self.case3_x = [163,765,141,166,137,355,136,1206,433,1130]  
        self.case3_y = [186,699,132,272,291,331,199,1890,788,1601] 


        self.case4_x = [163,765,141,166,137,355,136,1206,433,1130]  
        self.case4_y = [15,69.9,6.5,22.4,28.4,65.9,19.4,198.7,38.8,138.2]  


        self.x = self.case1_x[:]
        self.y = self.case1_y[:]
        self.n = len(self.x)


        try:
            self.pushButton.clicked.connect(self.case1)
            self.pushButton_3.clicked.connect(self.case2)
            self.pushButton_2.clicked.connect(self.case3)
            self.pushButton_4.clicked.connect(self.case4)
            self.pushButton_5.clicked.connect(self.calcular)
        except Exception:
            pass


    def calcular(self):

        txt = self.lineEdit.text().strip()
        try:
            xk = float(txt)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Introduce un valor numérico válido para XK en el campo superior.")
            return


        if not (hasattr(self, 'x') and hasattr(self, 'y')):
            QtWidgets.QMessageBox.warning(self, "Datos faltantes", "No hay datos para calcular. Usa los botones Case o configura los arrays x,y.")
            return
        if len(self.x) != len(self.y) or len(self.x) < 2:
            QtWidgets.QMessageBox.warning(self, "Datos inválidos", "Las listas x e y deben tener la misma longitud (>=2).")
            return


        try:
            calc = CalculadoraSum(self.x, self.y, len(self.x))
            b0, b1 = calc.calcula()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error cálculo", f"Error al calcular b0/b1: {e}")
            return


        try:
            n = calc.n
            sumx = calc.sumx
            sumy = calc.sumy
            sumxy = calc.sumxy
            sumx2 = calc.sumx2
            sumy2 = calc.sumy2


            numer = (n * sumxy) - (sumx * sumy)
            denom = ((n * sumx2 - sumx ** 2) * (n * sumy2 - sumy ** 2))
            if denom <= 0:
                R = 0.0
            else:
                import math


                R = numer / math.sqrt(denom)
            R2 = R ** 2
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error estadístico", f"No se pudo calcular R/R2: {e}")
            R = 0.0
            R2 = 0.0


        try:
            yk = b0 + b1 * xk
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error predicción", f"No se pudo calcular Yk: {e}")
            yk = 0.0
        # Guardar resultados como atributos de la instancia para que otras ventanas los usen
        self.b0 = b0
        self.b1 = b1
        self.R = R
        self.R2 = R2
        self.yk = yk
        fmt = lambda v: f"{v:.4f}"
        try:
            self.label_8.setText(fmt(b1))
            self.label_9.setText(fmt(b0))
            self.label_10.setText(fmt(R))
            self.label_11.setText(fmt(R2))
            self.label_12.setText(fmt(yk))
        except Exception as e:


            QtWidgets.QMessageBox.information(self, "Resultados", f"b1={b1}, b0={b0}, R={R}, R2={R2}, Yk={yk}\n\n(Se produjo un error al actualizar las etiquetas: {e})")


    def load_dataset(self, x_list, y_list, name=""):
        if not x_list or not y_list:
            QtWidgets.QMessageBox.warning(self, "Dataset vacío", f"El dataset {name} está vacío. Pegue las listas X e Y en el fichero fuente o use otro Case.")
            return
        if len(x_list) != len(y_list):
            QtWidgets.QMessageBox.warning(self, "Dataset inválido", f"X e Y deben tener la misma longitud para {name}.")
            return
        self.x = x_list[:]
        self.y = y_list[:]
        self.n = len(self.x)
        try:
            self.statusbar.showMessage(f"Dataset cargado: {name}")
        except Exception:
            pass


    def case1(self):
        self.load_dataset(self.case1_x, self.case1_y, "Case 1")
        


    def case2(self):
        self.load_dataset(self.case2_x, self.case2_y, "Case 2")


    def case3(self):
        self.load_dataset(self.case3_x, self.case3_y, "Case 3")


    def case4(self):
        self.load_dataset(self.case4_x, self.case4_y, "Case 4")
