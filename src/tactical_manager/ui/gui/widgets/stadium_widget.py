from __future__ import annotations

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
)

from tactical_manager.core.models import Stadium, StadiumSection


class ClickableSectionItem(QGraphicsRectItem):
    def __init__(
        self,
        section: StadiumSection,
        rect: QRectF,
        on_click,
    ) -> None:
        super().__init__(rect)
        self.section = section
        self._on_click = on_click
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event) -> None:
        self._on_click(self.section.name)
        super().mousePressEvent(event)


class StadiumWidget(QGraphicsView):
    section_selected = Signal(str)

    def __init__(self, stadium: Stadium):
        super().__init__()
        self.stadium = stadium
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self._section_items: dict[str, ClickableSectionItem] = {}
        self._selected_section_name: str | None = None

        self.setRenderHint(self.renderHints())
        self.setMinimumHeight(420)
        self.setObjectName("stadium_widget")

        self.refresh()

    def refresh(self) -> None:
        self.scene.clear()
        self._section_items.clear()

        self._draw_pitch()
        self._draw_sections()

        if self._selected_section_name:
            self._highlight_selected(self._selected_section_name)

    def set_selected_section(self, section_name: str | None) -> None:
        self._selected_section_name = section_name
        self._update_section_styles()

    def _draw_pitch(self) -> None:
        pitch_rect = QRectF(140, 110, 220, 140)

        pitch = self.scene.addRect(
            pitch_rect,
            QPen(QColor("#dcdcdc"), 2),
            QBrush(QColor("#2e8b57")),
        )

        center_line_x = pitch_rect.x() + pitch_rect.width() / 2
        self.scene.addLine(
            center_line_x,
            pitch_rect.y(),
            center_line_x,
            pitch_rect.y() + pitch_rect.height(),
            QPen(QColor("#dcdcdc"), 2),
        )

        center_circle_size = 36
        self.scene.addEllipse(
            center_line_x - center_circle_size / 2,
            pitch_rect.y() + pitch_rect.height() / 2 - center_circle_size / 2,
            center_circle_size,
            center_circle_size,
            QPen(QColor("#dcdcdc"), 2),
        )

        self.scene.addText("Pitch").setPos(230, 255)
        pitch.setZValue(0)

    def _draw_sections(self) -> None:
        section_map = self._section_layouts()

        for section in self.stadium.sections:
            rect = section_map.get(section.name)
            if rect is None:
                continue

            item = ClickableSectionItem(
                section=section,
                rect=rect,
                on_click=self._handle_section_clicked,
            )
            item.setPen(QPen(QColor("#222222"), 2))
            item.setBrush(QBrush(self._section_color(section)))
            self.scene.addItem(item)

            label = QGraphicsSimpleTextItem(
                f"{section.name}\n{section.capacity:,}"
            )
            label_rect = label.boundingRect()
            label.setPos(
                rect.x() + (rect.width() - label_rect.width()) / 2,
                rect.y() + (rect.height() - label_rect.height()) / 2,
            )
            self.scene.addItem(label)

            self._section_items[section.name] = item

        self._update_section_styles()

    def _section_layouts(self) -> dict[str, QRectF]:
        return {
            "North Stand": QRectF(150, 40, 200, 50),
            "South Stand": QRectF(150, 270, 200, 50),
            "West Stand": QRectF(60, 110, 60, 140),
            "East Stand": QRectF(380, 110, 60, 140),
        }

    def _handle_section_clicked(self, section_name: str) -> None:
        self._selected_section_name = section_name
        self._update_section_styles()
        self.section_selected.emit(section_name)

    def _update_section_styles(self) -> None:
        for name, item in self._section_items.items():
            section = item.section
            item.setBrush(QBrush(self._section_color(section)))

            if name == self._selected_section_name:
                item.setPen(QPen(QColor("#ffd24a"), 4))
            else:
                item.setPen(QPen(QColor("#222222"), 2))

    def _highlight_selected(self, section_name: str) -> None:
        self._selected_section_name = section_name
        self._update_section_styles()

    def _section_color(self, section: StadiumSection) -> QColor:
        if section.section_type == "vip":
            base = QColor("#d4af37")
        elif section.section_type == "standing":
            base = QColor("#5dade2")
        else:
            base = QColor("#7dcea0")

        if not section.covered:
            return base.darker(115)

        return base