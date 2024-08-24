import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
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

        # Connect functions to buttons
        self.ui.infoBtn.clicked.connect(self.__info_dialog)
        self.ui.getValues.clicked.connect(self.__get_values)
        self.ui.startPendulum.clicked.connect(self.start_movement)
        self.ui.reset.clicked.connect(self.oberbek_widget.reset_position)

    def start_movement(self):
        mass_text = self.ui.massEdit_M.text().strip()
        if not mass_text:
            QMessageBox.warning(self, "Ошибка", "Введите значение массы груза!")
            return

        try:
            mass = float(mass_text)
            self.oberbek_widget.start_movement(mass)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Масса груза должна быть числом!")

    def reset_movement(self):
        self.oberbek_widget.reset_position()

    # Get values function
    def __get_values(self):
        self.m = self.ui.massEdit_M.text()
        self.ui.textBrowser.setText("Ускорение падения груза: " +
                                    str(round(float(4400 - float(self.m) * g) / float(self.m), 2)) + " м/с^2\n" +
                                    "Угловое ускорение: " +
                                    str(round(float((4400 - float(self.m) * g) / float(self.m)) / R, 2)) + " c^-1\n" +
                                    "Момент инерции: " +
                                    str(round((((float(self.m) - 50) * g * R ** 2) / (2 * L)), 2))
                                    + " г * м^2\n"
        )

    @classmethod
    def __info_dialog(cls):
        cls.infoModal.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    MainWindow.infoModal = InfoModal()
    window.show()

    sys.exit(app.exec())
