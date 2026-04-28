from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QInputDialog
from psp.ejercicio4.ejercicio4 import calcular_sigma, calcular_rango, calcular_upi_lpi


class VentanaPSP4(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui/ventana_psp4.ui', self)

        # crear botón calcular dinámicamente y conectarlo
        self.btn_calcular = QtWidgets.QPushButton('Calcular', self)
        # colocarlo al final del layout central (aprox)
        try:
            self.centralWidget().layout().addWidget(self.btn_calcular)
        except Exception:
            pass
        self.btn_calcular.clicked.connect(self.calcular)

    def _ask_list(self, title, label):
        text, ok = QInputDialog.getText(self, title, label)
        if not ok:
            raise RuntimeError('Entrada cancelada')
        # interpretar como lista de floats separados por comas
        items = [s.strip() for s in text.split(',') if s.strip() != '']
        return [float(x) for x in items]

    def calcular(self):
        try:
            xk_txt = self.lineEdit.text().strip()
            n_txt = self.lineEdit_2.text().strip()
            if not xk_txt or not n_txt:
                QtWidgets.QMessageBox.warning(self, 'Faltan datos', 'Introduce xk y n en los campos superiores')
                return
            xk = float(xk_txt)
            n = int(float(n_txt))

            # pedir listas yi y xi al usuario (podemos obtenerlas automáticamente desde PSP1 si está abierta)
            yi = None
            xi = None

            # Intentar obtener b0,b1,yk desde la ventana del ejercicio1 si está abierta
            b0 = b1 = yk = None
            try:
                import importlib
                mp = importlib.import_module('load.load_menuPrincipal')
                main = getattr(mp, 'MenuPrincipal', None)
                # intentar obtener la instancia guardada en el módulo global (si existe)
                # nota: esto solo funcionará si el programa creó la instancia y la dejó en memoria
                inst = None
                if hasattr(mp, 'MenuPrincipal'):
                    # buscar variable global 'vc' en la instancia activa si existe
                    try:
                        # si hay una aplicación Qt, podemos recorrer topLevelWidgets
                        from PyQt5 import QtWidgets
                        for w in QtWidgets.QApplication.topLevelWidgets():
                            # buscar por clase nombre
                            if w.__class__.__name__ == 'VentanaCalculadoraSum':
                                inst = w
                                break
                    except Exception:
                        inst = None
                if inst is not None:
                    # Si la ventana 1 existe pero todavía no tiene b0/b1/yk, pedirle que calcule
                    try:
                        if not (hasattr(inst, 'b0') and hasattr(inst, 'b1') and hasattr(inst, 'yk')):
                            # colocar el xk en el lineEdit de la ventana 1 y llamarla a calcular()
                            try:
                                inst.lineEdit.setText(str(xk))
                                inst.calcular()
                            except Exception:
                                pass
                    except Exception:
                        pass

                    # preferir atributos calculados por la ventana 1 si existen
                    if hasattr(inst, 'b0') and hasattr(inst, 'b1'):
                        b0 = inst.b0
                        b1 = inst.b1
                    elif hasattr(inst, 'x') and hasattr(inst, 'y'):
                        # fallback: recalcular si solo tenemos x,y
                        from psp.ejercicio1.ejercicio1 import CalculadoraSum
                        calc = CalculadoraSum(inst.x, inst.y, inst.n)
                        b0, b1 = calc.calcula()
                    # yk preferido desde atributo
                    if hasattr(inst, 'yk'):
                        yk = inst.yk
                    # si la ventana 1 tiene los arrays x,y úsalos
                    if hasattr(inst, 'x') and hasattr(inst, 'y'):
                        xi = inst.x
                        yi = inst.y
            except Exception:
                b0 = b1 = yk = None

            # No pedir b0,b1,yk: calcularlos si no vinieron desde PSP1
            source = None
            try:
                if (b0 is None or b1 is None) and (xi is not None and yi is not None):
                    # calcular b0,b1 desde xi,yi
                    from psp.ejercicio1.ejercicio1 import CalculadoraSum
                    calc = CalculadoraSum(xi, yi, len(xi))
                    b0, b1 = calc.calcula()
                    source = 'calculado desde xi/yi'

                # Si aún no tenemos b0/b1, intentar usar dataset por defecto (Case1)
                if b0 is None or b1 is None:
                    xi = [130,650,99,150,128,302,95,945,368,961]
                    yi = [186,699,132,272,291,331,199,1890,788,1601]
                    try:
                        from psp.ejercicio1.ejercicio1 import CalculadoraSum
                        calc = CalculadoraSum(xi, yi, len(xi))
                        b0, b1 = calc.calcula()
                        source = 'calculado desde dataset por defecto (Case1)'
                    except Exception as e:
                        raise RuntimeError(f'No se pudieron calcular b0/b1 ni desde xi/yi ni desde el dataset por defecto: {e}')

                # calcular yk automáticamente
                yk = b0 + b1 * xk
                # informar al usuario de la fuente usada
                if source:
                    QtWidgets.QMessageBox.information(self, 'Información', f'b0/b1 obtenidos: {source}')
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error cálculo b0/b1', str(e))
                return

            # si no obtuvimos xi/yi desde la ventana 1, usar dataset por defecto (Case1)
            if xi is None or yi is None:
                QtWidgets.QMessageBox.information(self, 'Dataset por defecto', 'No se encontraron listas xi/yi; se usará el dataset Case1 por defecto.')
                xi = [130,650,99,150,128,302,95,945,368,961]
                yi = [186,699,132,272,291,331,199,1890,788,1601]

            # asegurar que tval exista (si no fue pedido antes)
            if 'tval' not in locals():
                tval_txt, ok = QInputDialog.getText(self, 't', 'Introduce t (por ejemplo t(0.35, dof)):')
                if not ok:
                    return
                tval = float(tval_txt)

            # calcular sigma devuelve (sigma, sumax, xavg)
            sigma, sumax, xavg = calcular_sigma(n, yi, b0, b1, xi)
            rango = calcular_rango(tval, sigma, n, xk, xavg, sumax)
            upi, lpi = calcular_upi_lpi(yk, rango)

            # mostrar resultados en labels (label_11..label_18 están en el .ui)
            try:
                self.label_11.setText(f'{sigma:.6f}')
                self.label_12.setText(f'{rango:.6f}')
                self.label_13.setText(f'{upi:.6f}')
                self.label_14.setText(f'{lpi:.6f}')
                self.label_15.setText(str(b0))
                self.label_16.setText(str(b1))
                self.label_17.setText(str(yk))
                self.label_18.setText(str(tval))
            except Exception:
                pass

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Error al calcular: {e}')
