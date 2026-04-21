from PyQt5 import QtWidgets
import sys

from load.load_menuPrincipal import MenuPrincipal

def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()