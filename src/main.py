import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QWidget
from mainUI import Ui_MainWindow
from modalInfo import Ui_Dialog

from oberbek import *


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

    @classmethod
    def __info_dialog(cls):
        cls.infoModal.show()

    def __get_values(self):
        r = 0.022
        g = 9.81
        T = 1500
        m = self.ui.massEdit_M.text()
        self.ui.textBrowser.setText("Вращающий момент: " + str(round((float(m) * float(g) * float(r)), 2)) + " Н * м" +
                                    '\n' +
                                    "Ускорение: " + str(round((T - float(m) * float(g)) / float(m), 2)) + " м / с^2" +
                                    '\n' +
                                    "Момент инерции маятника: " + str(round(
                    ((float(m) - 0.005) * g * r ** 2 * 5.0 ** 2) / (2.0 * 0.5) - float(m) * r ** 2, 2)) + " кг * м^2"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    MainWindow.infoModal = InfoModal()
    window.show()

    sys.exit(app.exec())
