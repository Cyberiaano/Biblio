import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from connection import Ui_Dialog
from Gestion import Ui_MainWindow

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.open_main_window)

    def open_main_window(self):
        self.main_window = QMainWindow()
        self.ui_main = Ui_MainWindow()
        self.ui_main.setupUi(self.main_window)
        self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
