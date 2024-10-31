from PySide6.QtWidgets import QScrollArea, QWidget, QLabel
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QDropEvent


class CentralScrollArea(QScrollArea):
    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)

        self.setWidget(CentralScrollAreaWidget(self))


class CentralScrollAreaWidget(QWidget):
    def __init__(self, parent: QWidget | None = ...):
        super().__init__(parent)

        self.setAcceptDrops(True)

        self.item_widgets = []
        self.main_window = None


    def move_item_widget(self, old_idx : int, new_idx : int):
        if (new_idx >= len(self.item_widgets) or new_idx < 0):
            return
        
        widget = self.item_widgets.pop(old_idx)
        self.item_widgets.insert(new_idx, widget)

        self.layout().removeWidget(widget)
        self.layout().insertWidget(new_idx, widget)


    def dragEnterEvent(self, event: QDragEnterEvent):
        event.accept()


    def dragLeaveEvent(self, event: QDragLeaveEvent):
        event.accept()


    def dragMoveEvent(self, event: QDragMoveEvent):
        print(self.get_drop_index(event))
        event.accept()


    def dropEvent(self, event : QDropEvent):
        drop_idx = self.get_drop_index(event)
        if drop_idx is None:
            return
        widget = event.source()
        start_idx = self.item_widgets.index(widget)
        if start_idx < drop_idx:
            self.move_item_widget(start_idx, drop_idx - 1)
        else:
            self.move_item_widget(start_idx, drop_idx)
        event.accept()


    def get_drop_index(self, event):
        pos = event.position()
        spacing = self.layout().spacing()

        for n in range(len(self.item_widgets) + 1):
            rect = self.layout().itemAt(n).geometry()
            if pos.y() >= rect.y() - spacing - rect.height() / 2 and pos.y() <= rect.y() + rect.height() / 2:
                return n
        return None