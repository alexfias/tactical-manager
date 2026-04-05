from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QSlider, QVBoxLayout, QWidget, QCheckBox


class SettingsPage(QWidget):
    volume_changed = Signal(int)   # 0–100
    mute_toggled = Signal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # Title
        title = QLabel("Settings")
        title.setProperty("sectionTitle", True)
        layout.addWidget(title)

        # --- Audio section ---
        audio_title = QLabel("Audio")
        audio_title.setStyleSheet("font-weight: bold; color: white;")
        layout.addWidget(audio_title)

        # Volume label
        self.volume_label = QLabel("Volume: 30%")
        layout.addWidget(self.volume_label)

        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(30)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        layout.addWidget(self.volume_slider)

        # Mute toggle
        self.mute_checkbox = QCheckBox("Mute music")
        self.mute_checkbox.toggled.connect(self.mute_toggled.emit)
        layout.addWidget(self.mute_checkbox)

        layout.addStretch()

    def _on_volume_changed(self, value: int) -> None:
        self.volume_label.setText(f"Volume: {value}%")
        self.volume_changed.emit(value)

    def set_audio_state(self, volume: int, muted: bool) -> None:
        """Initialize UI from current audio settings"""
        self.volume_slider.blockSignals(True)
        self.mute_checkbox.blockSignals(True)

        self.volume_slider.setValue(volume)
        self.volume_label.setText(f"Volume: {volume}%")
        self.mute_checkbox.setChecked(muted)

        self.volume_slider.blockSignals(False)
        self.mute_checkbox.blockSignals(False)