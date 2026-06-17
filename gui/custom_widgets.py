from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsDropShadowEffect
)

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QIcon


# =====================================================
# GLOW EFFECT
# =====================================================

def create_glow(color="#00D4FF", blur=25):
    shadow = QGraphicsDropShadowEffect()

    shadow.setBlurRadius(blur)
    shadow.setOffset(0, 0)
    shadow.setColor(QColor(color))

    return shadow


# =====================================================
# GLASS CARD
# =====================================================

class GlassCard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("card")
        self.setGraphicsEffect(
            create_glow("#00D4FF", 20)
        )


# =====================================================
# DASHBOARD CARD
# =====================================================

class DashboardStatCard(QWidget):

    def __init__(self, title, value="0", parent=None):
        super().__init__(parent)

        self.setObjectName("card")

        self.title_label = QLabel(title)
        self.title_label.setObjectName("cardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("cardValue")

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.value_label)

        self.setLayout(layout)

        self.setMinimumHeight(100)

        #self.setGraphicsEffect(
         #   create_glow("#00D4FF", 25)
        #)

    def set_value(self, value):
        self.value_label.setText(str(value))


# =====================================================
# SIDEBAR BUTTON
# =====================================================

class SidebarButton(QPushButton):

    def __init__(self, text, icon_path=None):
        super().__init__(text)

        self.setObjectName("navButton")
        self.setCursor(Qt.PointingHandCursor)

        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(self.iconSize())


# =====================================================
# STATUS LABEL
# =====================================================

class NeonStatusLabel(QLabel):

    def __init__(self, text="SAFE", status="safe"):
        super().__init__(text)

        self.update_status(status)

    def update_status(self, status):

        status = status.lower()

        if status == "safe":

            self.setObjectName("safeLabel")

            self.setGraphicsEffect(
                create_glow("#00FF99", 30)
            )

        elif status == "modified":

            self.setObjectName("modifiedLabel")

            self.setGraphicsEffect(
                create_glow("#FF4D4D", 30)
            )

        elif status == "missing":

            self.setObjectName("missingLabel")

            self.setGraphicsEffect(
                create_glow("#FFA500", 30)
            )

        self.style().unpolish(self)
        self.style().polish(self)


# =====================================================
# CYBER TITLE BAR
# =====================================================

class CyberTitleBar(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent

        self.setObjectName("titleBar")
        self.setFixedHeight(55)

        self.drag_position = QPoint()

        self.title = QLabel("CyberSentinel FIM")
        self.title.setObjectName("titleLabel")

        self.min_btn = QPushButton("—")
        self.max_btn = QPushButton("□")
        self.close_btn = QPushButton("✕")

        for btn in [self.min_btn, self.max_btn, self.close_btn]:
            btn.setFixedSize(35, 30)

        self.close_btn.clicked.connect(
            self.parent_window.close
        )

        self.min_btn.clicked.connect(
            self.parent_window.showMinimized
        )

        self.max_btn.clicked.connect(
            self.toggle_maximize
        )

        layout = QHBoxLayout()

        layout.addWidget(self.title)
        layout.addStretch()

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def toggle_maximize(self):

        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()

    # -----------------------------
    # Drag Window
    # -----------------------------

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.drag_position = (
                event.globalPos()
                - self.parent_window.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.LeftButton:

            self.parent_window.move(
                event.globalPos() - self.drag_position
            )

            event.accept()


# =====================================================
# MONITOR STATUS WIDGET
# =====================================================

class MonitorStatusWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.status_label = QLabel(
            "●  Monitoring Stopped"
        )

        self.status_label.setObjectName(
            "monitorStatus"
        )

        self.status_label.setGraphicsEffect(
            create_glow("#00FF99", 25)
        )

        layout = QHBoxLayout()

        layout.addWidget(self.status_label)
        layout.addStretch()

        self.setLayout(layout)

    def set_active(self):

        self.status_label.setText(
            "● Real-Time Monitoring Active"
        )

    def set_inactive(self):

        self.status_label.setText(
            "● Real-Time Monitoring Stopped"
        )


# =====================================================
# LOGO HEADER
# =====================================================

class LogoHeader(QWidget):

    def __init__(self, logo_label="CyberSentinel"):
        super().__init__()

        self.setObjectName("logoContainer")

        self.logo = QLabel()

        self.logo.setFixedSize(50, 50)
        self.logo.setAlignment(Qt.AlignCenter)

        self.text = QLabel(logo_label)
        self.text.setObjectName("logoText")

        layout = QHBoxLayout()

        layout.addWidget(self.logo)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def set_logo(self, pixmap):
        self.logo.setPixmap(pixmap)