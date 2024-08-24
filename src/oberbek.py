import numpy as np

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtGui import QPainter, QBrush, QColor

# Parameters
L = 100
R = 10
g = 9.81
k = 0.01
vM = 50

offset_x = 75


class Oberbek(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = np.pi / 4
        self.omega = 0
        self.dt = 0.05
        self.moment_arm = 0
        self.rotation_angle = 0
        self.movement_enabled = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_oberbek)

    def start_movement(self, mass):
        if mass <= 0:
            QMessageBox.warning(self, "Ошибка", "Масса груза должна быть положительным числом!")
            return

        self.movement_enabled = True
        if not self.timer.isActive():
            self.timer.start(30)

    def update_oberbek(self):
        if not self.movement_enabled:
            return

        alpha = - (g / L) * np.sin(self.angle) - k * self.omega
        self.omega += alpha * self.dt
        self.angle += self.omega * self.dt
        self.moment_arm += vM * self.dt
        if self.moment_arm >= self.height() - 300:
            self.movement_enabled = False
            self.timer.stop()
        self.rotation_angle += self.dt
        self.update()

    def reset_position(self):
        self.angle = np.pi / 4
        self.omega = 0
        self.moment_arm = 0
        self.rotation_angle = 0
        self.movement_enabled = False
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        center_x = self.width() // 2
        center_y = self.height() // 4
        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.drawLine(center_x, center_y, center_x, self.height() - 50)
        base_center_y = self.height() - 50
        base_width = 150
        base_height = 20
        painter.drawRect(center_x - base_width // 2, base_center_y, base_width, base_height)
        painter.setBrush(QBrush(QColor(150, 150, 150)))
        painter.drawEllipse(center_x - R, center_y - R, 2 * R, 2 * R)
        end_x = center_x + offset_x
        end_y = center_y + self.moment_arm
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(end_x - 10, end_y - 10, 20, 20)
        for i in range(4):
            angle_spike = self.rotation_angle + i * np.pi / 2
            pivot_x = center_x + int(R * np.sin(angle_spike))
            pivot_y = center_y + int(R * np.cos(angle_spike))
            mass_x = center_x + int((L + R) * np.sin(self.angle + angle_spike))
            mass_y = center_y + int((L + R) * np.cos(self.angle + angle_spike))
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawLine(center_x, center_y, mass_x, mass_y)
            painter.setBrush(QBrush(QColor(0, 0, 255)))
            painter.drawRect(mass_x - 5, mass_y - 5, 10, 10)
