from PyQt5 import QtWidgets, uic
import os
import sys

from psp.ejercicio3.ejercicio3 import Findx


class VentanaPSP3(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/ventana_psp3.ui", self)
        try:
            self.pushButton.clicked.connect(self.on_calcular)
        except Exception:
            pass

    def on_calcular(self):
        try:
            tol_txt = self.lineEdit.text().strip()
            p_txt = self.lineEdit_2.text().strip()
            dof_txt = self.lineEdit_3.text().strip()
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Error UI", "No se encontraron los campos en la UI")
            return

        try:
            tol = float(tol_txt) if tol_txt != '' else 1e-6
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Introduce una tolerancia válida")
            return

        try:
            p = float(p_txt)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Introduce un valor numérico válido para p")
            return

        try:
            dof = float(dof_txt)
        except Exception:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Introduce un DOF válido")
            return

        x0 = 1.0
        d0 = 0.5
        n = 100

        try:
            finder = Findx(dof=dof)
            x_res, p_res, its = finder.find_x(p_target=p, x0=x0, d0=d0, tol=tol, n=n)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error cálculo", f"No se pudo calcular x: {e}")
            return

        try:
            self.label_4.setText(f"x={x_res:.10f}\np={p_res:.10f}\niter={its}")
        except Exception:
            try:
                self.label_4.setText(str(x_res))
            except Exception:
                pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = VentanaPSP3()
    w.show()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets, uic
from psp.ejercicio3.ejercicio3 import Findx


class VentanaPSP3(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('gui/ventana_psp3.ui', self)
		try:
			self.pushButton.clicked.connect(self.calcular)
		except Exception:
			pass

	def calcular(self):
		try:
			tol_txt = self.lineEdit.text().strip()
			p_txt = self.lineEdit_2.text().strip()
			dof_txt = self.lineEdit_3.text().strip()
		except Exception:
			QtWidgets.QMessageBox.warning(self, 'Error UI', 'Campos de entrada no encontrados')
			return

		try:
			tol = float(tol_txt) if tol_txt != '' else 1e-6
		except Exception:
			QtWidgets.QMessageBox.warning(self, 'Entrada inválida', 'Introduce una tolerancia numérica válida')
			return

		try:
			p = float(p_txt)
		except Exception:
			QtWidgets.QMessageBox.warning(self, 'Entrada inválida', 'Introduce un número válido para p')
			return

		try:
			dof = float(dof_txt)
		except Exception:
			QtWidgets.QMessageBox.warning(self, 'Entrada inválida', 'Introduce un número válido para dof')
			return

		x0 = 1.0
		d0 = 0.5
		n = 100

		finder = Findx(dof=dof)
		try:
			x_res, p_res, its = finder.find_x(p_target=p, x0=x0, d0=d0, tol=tol, n=n)
		except Exception as e:
			QtWidgets.QMessageBox.critical(self, 'Error cálculo', f'Error al calcular: {e}')
			return

		try:
			self.label_4.setText(str(x_res))
		except Exception:
			try:
				self.label_resultado.setText(str(x_res))
			except Exception:
				pass


if __name__ == '__main__':
	app = QtWidgets.QApplication([])
	w = VentanaPSP3()
	w.show()
	app.exec_()

