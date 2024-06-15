"""Модуль запуска программы"""

import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSize

from gui.simulation import CollisionSimulation
from gui.settings import SettingsWindow


class MainWindow(QMainWindow):
    """Запуск приложения"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Asteroid simulator")

        self.simulation_window = CollisionSimulation()
        self.simulation_window.setMinimumSize(QSize(120, 40))
        self.settings_window = SettingsWindow()
        self.settings_window.settings_changed.connect(
            self.simulation_window.generate_balls
        )
        self.simulation_window.window_resized.connect(self.settings_window.update_size)

        self.setCentralWidget(self.simulation_window)
        self.settings_window.show()
        self.simulation_window.show()
        self.settings_window.destroyed.connect(self.close)

    def closeEvent(self, event):
        """Метод вызывается при закрытии главного окна."""
        QApplication.quit()


if __name__ == "__main__":
    # Главная точка входа в приложение.
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
