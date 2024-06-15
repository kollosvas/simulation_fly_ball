"""Модуль окна настройки моделирования"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton
from PySide6.QtCore import Signal, Slot


class SettingsWindow(QWidget):
    """Окно настройки"""

    settings_changed = Signal(int, int, int, int, int, int, int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setMinimumWidth(215)
        self.setMaximumWidth(215)
        self.setMinimumHeight(400)
        self.setMaximumHeight(400)
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Количество шаров:"))
        self.num_balls_spinbox = QSpinBox()
        self.num_balls_spinbox.setMaximum(200)
        self.num_balls_spinbox.setMinimum(1)
        self.num_balls_spinbox.setValue(1)
        layout.addWidget(self.num_balls_spinbox)

        layout.addWidget(QLabel("Мин. размер шара:"))
        self.min_radius_spinbox = QSpinBox()
        self.min_radius_spinbox.setMinimum(1)
        self.min_radius_spinbox.setMaximum(30)
        self.min_radius_spinbox.setValue(5)
        layout.addWidget(self.min_radius_spinbox)

        layout.addWidget(QLabel("Макс. размер шара:"))
        self.max_radius_spinbox = QSpinBox()
        self.max_radius_spinbox.setMinimum(1)
        self.max_radius_spinbox.setMaximum(30)
        self.max_radius_spinbox.setValue(15)
        layout.addWidget(self.max_radius_spinbox)

        layout.addWidget(QLabel("Ширина области:"))
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setMinimum(40)
        self.width_spinbox.setMaximum(1900)
        self.width_spinbox.setValue(800)
        self.width_spinbox.setReadOnly(True)
        layout.addWidget(self.width_spinbox)

        layout.addWidget(QLabel("Высота области:"))
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setMinimum(40)
        self.height_spinbox.setMaximum(900)
        self.height_spinbox.setValue(600)
        self.height_spinbox.setReadOnly(True)
        layout.addWidget(self.height_spinbox)

        layout.addWidget(QLabel("Мин. скорость:"))
        self.min_speed_spinbox = QSpinBox()
        self.min_speed_spinbox.setMinimum(1)
        self.min_speed_spinbox.setMaximum(20)
        self.min_speed_spinbox.setValue(1)
        layout.addWidget(self.min_speed_spinbox)

        layout.addWidget(QLabel("Макс. скорость:"))
        self.max_speed_spinbox = QSpinBox()
        self.max_speed_spinbox.setMinimum(1)
        self.max_speed_spinbox.setMaximum(20)
        self.max_speed_spinbox.setValue(5)
        layout.addWidget(self.max_speed_spinbox)

        generate_button = QPushButton("Сгенерировать шары")
        generate_button.clicked.connect(self.on_generate)
        layout.addWidget(generate_button)

        self.setLayout(layout)

    @Slot()
    def on_generate(self):
        """Слот, который вызывается при нажатии кнопки генерации шаров."""
        self.settings_changed.emit(
            self.num_balls_spinbox.value(),
            self.min_radius_spinbox.value(),
            self.max_radius_spinbox.value(),
            self.width_spinbox.value(),
            self.height_spinbox.value(),
            self.min_speed_spinbox.value(),
            self.max_speed_spinbox.value(),
        )

    @Slot(int, int)
    def update_size(self, width, height):
        """Слот, который обновляет значения ширины и высоты области в спинбоксах."""
        self.width_spinbox.setValue(width)
        self.height_spinbox.setValue(height)
