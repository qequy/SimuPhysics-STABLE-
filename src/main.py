import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QDialog
from mainUI import Ui_MainWindow
from modalInfo import Ui_Dialog

from oberbek import *

# Parameters from `oberbek.py`
L = 100
R = 10
g = 9.81
k = 0.01
vM = 50

class InfoModal(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        self.oberbek_widget = Oberbek()

        self.oberbek_widget.setMinimumSize(500, 500)
        self.ui.oberbekLayout.addWidget(self.oberbek_widget)

        self.ui.infoBtn.clicked.connect(self.__info_dialog)
        self.ui.getValues.clicked.connect(self.__get_values)
        self.ui.startPendulum.clicked.connect(self.oberbek_widget.start_movement)
        self.ui.reset.clicked.connect(self.oberbek_widget.reset_position)

    # ----------------------- #
    # Functions to get values #
    # ----------------------- #
    def __get_values(self):
        self.m = self.ui.massEdit_M.text()
        self.ui.textBrowser.setText("Ускорение падения груза: " +
                                    str(round(float(4400 - float(self.m) * g) / float(self.m), 2)) + " м/с^2" + '\n' +
                                    "Угловое ускорение: " +
                                    str(round(float((4400 - float(self.m) * g) / float(self.m)) / R, 2)) + " c^-1" + '\n' +
                                    "Момент инерции: " +
                                    str(round((self.m - (g - (4400 - float(self.m) * g) / float(self.m) * R) / 4400 - float(self.m) * g) / float(self.m))), 2)

    @classmethod
    def __info_dialog(cls):
        cls.infoModal.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    MainWindow.infoModal = InfoModal()
    window.show()

    sys.exit(app.exec())
