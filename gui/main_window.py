from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QFrame,
    QStackedWidget,
    QTableWidget,
    QTextEdit,
    QLineEdit,
    QTableWidgetItem,
    QHeaderView
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import os

from gui.styles import CYBER_STYLE

from gui.custom_widgets import (
    DashboardStatCard,
    SidebarButton,
    CyberTitleBar,
    MonitorStatusWidget,
    LogoHeader
)

from core.hash_manager import HashManager
from core.database import DatabaseManager
from core.logger import ActivityLogger
from core.realtime_monitor import RealTimeMonitor


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.db = DatabaseManager()
        self.logger = ActivityLogger()

        self.monitor = None

        self.init_ui()

    # ==================================================
    # UI SETUP
    # ==================================================

    def init_ui(self):

        self.setWindowTitle("CyberSentinel FIM")

        self.setMinimumSize(1400, 850)

        self.setWindowFlags(
            Qt.FramelessWindowHint
        )

        self.setStyleSheet(CYBER_STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # --------------------------------------
        # Sidebar
        # --------------------------------------

        self.sidebar = self.create_sidebar()

        # --------------------------------------
        # Content Area
        # --------------------------------------

        content_layout = QVBoxLayout()

        self.title_bar = CyberTitleBar(self)

        self.pages = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.monitor_page = self.create_monitor_page()
        self.logs_page = self.create_logs_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.monitor_page)
        self.pages.addWidget(self.logs_page)

        content_layout.addWidget(self.title_bar)
        content_layout.addWidget(self.pages)

        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(content_layout)

        self.refresh_dashboard()
        self.connect_signals()
        self.initialize_services()

    # ==================================================
    # SIDEBAR
    # ==================================================

    def create_sidebar(self):

        sidebar = QFrame()

        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)

        # --------------------------------------
        # Logo
        # --------------------------------------

        self.logo_header = LogoHeader(
            "CyberSentinel"
        )

        logo_path = "assets/logo.png"

        if os.path.exists(logo_path):

            pixmap = QPixmap(logo_path)

            self.logo_header.set_logo(
                pixmap.scaled(
                    48,
                    48,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        layout.addWidget(self.logo_header)

        layout.addSpacing(20)

        # --------------------------------------
        # Navigation Buttons
        # --------------------------------------

        self.dashboard_btn = SidebarButton(
            "Dashboard",
            "assets/icons/dashboard.png"
        )

        self.browse_btn = SidebarButton(
            "Browse File",
            "assets/icons/browse.png"
        )

        self.verify_btn = SidebarButton(
            "Verify Integrity",
            "assets/icons/verify.png"
        )
        self.monitor_btn = SidebarButton(
            "Start Monitoring",
            "assets/icons/monitor.png"
        )
        

        self.update_btn = SidebarButton(
            "Update Baseline",
            "assets/icons/update.png"
        )

        self.remove_btn = SidebarButton(
            "Remove File",
            "assets/icons/remove.png"
        )

        self.logs_btn = SidebarButton(
            "Activity Logs",
            "assets/icons/logs.png"
        )

        # --------------------------------------

        self.dashboard_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.logs_btn.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.verify_btn)
        layout.addWidget(self.monitor_btn)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.remove_btn)
        layout.addWidget(self.logs_btn)

        layout.addStretch()

        # --------------------------------------
        # Real Time Status
        # --------------------------------------

        self.monitor_status = MonitorStatusWidget()

        layout.addWidget(self.monitor_status)

        return sidebar

    # ==================================================
    # DASHBOARD PAGE
    # ==================================================

    def create_dashboard_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        # --------------------------------------
        # Stats Cards
        # --------------------------------------

        cards_layout = QHBoxLayout()

        self.monitored_card = DashboardStatCard(
            "Monitored Files",
            "0"
        )

        self.safe_card = DashboardStatCard(
            "Safe Files",
            "0"
        )

        self.modified_card = DashboardStatCard(
            "Modified Files",
            "0"
        )

        cards_layout.addWidget(
            self.monitored_card
        )

        cards_layout.addWidget(
            self.safe_card
        )

        cards_layout.addWidget(
            self.modified_card
        )

        layout.addLayout(cards_layout)

        # --------------------------------------
        # Search
        # --------------------------------------

        self.search_box = QLineEdit()

        self.search_box.setPlaceholderText(
            "Search monitored files..."
        )

        layout.addWidget(self.search_box)

        # --------------------------------------
        # Table
        # --------------------------------------

        self.files_table = QTableWidget()

        self.files_table.setColumnCount(5)

        self.files_table.setHorizontalHeaderLabels(
            [
                "File Name",
                "Path",
                "Status",
                "SHA256",
                "Date Added"
            ]
        )

        self.files_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        layout.addWidget(self.files_table)

        return page

    # ==================================================
    # MONITOR PAGE
    # ==================================================

    def create_monitor_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel(
            "File Integrity Operations"
        )

        title.setObjectName("titleLabel")

        layout.addWidget(title)

        self.operations_status = QLabel(
            "Ready"
        )

        layout.addWidget(
            self.operations_status
        )

        layout.addStretch()

        return page

    # ==================================================
    # LOG PAGE
    # ==================================================

    def create_logs_page(self):

        page = QWidget()

        layout = QVBoxLayout(page)

        title = QLabel(
            "Activity Logs"
        )

        title.setObjectName(
            "titleLabel"
        )

        layout.addWidget(title)

        self.log_viewer = QTextEdit()

        self.log_viewer.setReadOnly(True)

        layout.addWidget(
            self.log_viewer
        )

        return page
        # ==================================================
    # BUTTON CONNECTIONS
    # ==================================================

    def connect_signals(self):

        self.browse_btn.clicked.connect(
            self.browse_file
        )
        self.monitor_btn.clicked.connect(
            self.start_monitoring
        )

        self.verify_btn.clicked.connect(
            self.verify_integrity
        )

        self.update_btn.clicked.connect(
            self.update_baseline
        )

        self.remove_btn.clicked.connect(
            self.remove_selected_file
        )

        self.search_box.textChanged.connect(
            self.filter_table
        )

    # ==================================================
    # BROWSE FILE
    # ==================================================

    def browse_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File"
        )

        if not file_path:
            return

        sha256 = HashManager.generate_sha256(
            file_path
        )

        if not sha256:

            QMessageBox.warning(
                self,
                "Error",
                "Unable to generate SHA256 hash."
            )

            return

        self.db.add_file(
            file_path,
            sha256
        )

        self.logger.log(
            f"File Added: {file_path}"
        )

        QMessageBox.information(
            self,
            "Success",
            "File added to monitoring."
        )

        self.populate_table()
        self.refresh_dashboard()

    # ==================================================
    # POPULATE TABLE
    # ==================================================

    def populate_table(self):

        data = self.db.get_all_files()

        self.files_table.setRowCount(0)

        row = 0

        for path, info in data.items():

            self.files_table.insertRow(row)

            file_name = os.path.basename(path)

            status = info.get(
                "status",
                "SAFE"
            )

            self.files_table.setItem(
                row,
                0,
                QTableWidgetItem(file_name)
            )

            self.files_table.setItem(
                row,
                1,
                QTableWidgetItem(path)
            )

            self.files_table.setItem(
                row,
                2,
                QTableWidgetItem(status)
            )

            self.files_table.setItem(
                row,
                3,
                QTableWidgetItem(
                    info.get("hash", "")
                )
            )

            self.files_table.setItem(
                row,
                4,
                QTableWidgetItem(
                    info.get(
                        "date_added",
                        "-"
                    )
                )
            )

            row += 1

    # ==================================================
    # SEARCH TABLE
    # ==================================================

    def filter_table(self):

        search_text = (
            self.search_box.text()
            .lower()
            .strip()
        )

        for row in range(
            self.files_table.rowCount()
        ):

            visible = False

            for col in range(
                self.files_table.columnCount()
            ):

                item = self.files_table.item(
                    row,
                    col
                )

                if item:

                    if search_text in item.text().lower():
                        visible = True
                        break

            self.files_table.setRowHidden(
                row,
                not visible
            )

    # ==================================================
    # VERIFY INTEGRITY
    # ==================================================

    def verify_integrity(self):

        data = self.db.get_all_files()

        safe_count = 0
        modified_count = 0

        for path, info in data.items():

            if not os.path.exists(path):

                modified_count += 1

                self.logger.log(
                    f"Missing File: {path}"
                )

                continue

            current_hash = (
                HashManager.generate_sha256(
                    path
                )
            )

            if current_hash == info["hash"]:

                safe_count += 1

                self.db.update_status(
                    path,
                    "SAFE"
                )

            else:

                modified_count += 1

                self.db.update_status(
                    path,
                    "MODIFIED"
                )

                self.logger.log(
                    f"Integrity Violation: {path}"
                )

        self.populate_table()
        self.refresh_dashboard()
        self.load_logs()

        QMessageBox.information(
            self,
            "Verification Complete",
            f"Safe Files: {safe_count}\n"
            f"Modified Files: {modified_count}"
        )

    # ==================================================
    # UPDATE BASELINE
    # ==================================================

    def update_baseline(self):

        row = self.files_table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Selection Required",
                "Select a file first."
            )

            return

        file_path = (
            self.files_table.item(
                row,
                1
            ).text()
        )

        if not os.path.exists(file_path):

            QMessageBox.warning(
                self,
                "Error",
                "File no longer exists."
            )

            return

        reply = QMessageBox.question(
            self,
            "Update Baseline",
            "Replace stored hash with current hash?"
        )

        if reply != QMessageBox.Yes:
            return

        new_hash = (
            HashManager.generate_sha256(
                file_path
            )
        )

        self.db.update_hash(
            file_path,
            new_hash
        )

        self.logger.log(
            f"Baseline Updated: {file_path}"
        )

        self.populate_table()

        QMessageBox.information(
            self,
            "Updated",
            "Baseline updated successfully."
        )

    # ==================================================
    # REMOVE FILE
    # ==================================================

    def remove_selected_file(self):

        row = self.files_table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Selection Required",
                "Select a file first."
            )

            return

        file_path = (
            self.files_table.item(
                row,
                1
            ).text()
        )

        reply = QMessageBox.question(
            self,
            "Remove File",
            f"Remove monitoring for:\n\n{file_path}"
        )

        if reply != QMessageBox.Yes:
            return

        self.db.remove_file(
            file_path
        )

        self.logger.log(
            f"File Removed: {file_path}"
        )

        self.populate_table()
        self.refresh_dashboard()

    # ==================================================
    # LOAD LOGS
    # ==================================================

    def load_logs(self):

        log_path = "data/activity.log"

        if not os.path.exists(log_path):

            self.log_viewer.clear()
            return

        try:

            with open(
                log_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.log_viewer.setPlainText(
                    file.read()
                )

        except Exception as e:

            self.log_viewer.setPlainText(
                str(e)
            )

    # ==================================================
    # DASHBOARD REFRESH
    # ==================================================

    def refresh_dashboard(self):

        monitored = self.db.total_files()

        safe_count = self.db.count_safe()

        modified_count = (
            self.db.count_modified()
            +
            self.db.count_missing()
        )

        self.monitored_card.set_value(
            monitored
        )

        self.safe_card.set_value(
            safe_count
        )

        self.modified_card.set_value(
            modified_count
        )

        self.populate_table()

        self.load_logs()
       
    # ==================================================
    # REAL-TIME MONITORING
    # ==================================================

    def start_monitoring(self):

        data = self.db.get_all_files()

        if not data:

            QMessageBox.warning(
                self,
                "No Files",
                "Add files before starting monitoring."
            )

            return

        folders = set()

        for path in data.keys():

            if os.path.exists(path):

                folder = os.path.dirname(path)

                if folder:
                    folders.add(folder)

        if not folders:

            QMessageBox.warning(
                self,
                "Error",
                "No valid folders found."
            )

            return

        try:

            self.monitor = RealTimeMonitor()
            self.monitor.signals.integrity_alert.connect(
                self.show_alert
            )

            self.monitor.signals.refresh_required.connect(
                self.refresh_dashboard
            )

            self.monitor.signals.file_modified.connect(
                self.handle_file_modified
            )

            self.monitor.signals.file_deleted.connect(
                self.handle_file_deleted
            )

            self.monitor.signals.file_restored.connect(
                self.handle_file_restored
            )

            for folder in folders:
                self.monitor.start(folder)

            self.monitor_status.set_active()

            self.logger.log(
                "Real-Time Monitoring Started"
            )

            self.load_logs()

            QMessageBox.information(
                self,
                "Monitoring Started",
                "Real-time monitoring is active."
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Monitoring Error",
                str(e)
            )
        

        for folder in folders:
            print("Monitoring Folder:", folder)
            self.monitor.start(folder)

        self.show_alert(
        "Test Alert",
        "Monitoring Started Successfully"
        )

    # ==================================================
    # STOP MONITORING
    # ==================================================

    def stop_monitoring(self):

        try:

            if self.monitor:

                self.monitor.stop()

                self.monitor = None

                self.monitor_status.set_inactive()

                self.logger.log(
                    "Real-Time Monitoring Stopped"
                )

                self.load_logs()

        except Exception as e:

            print(e)

    # ==================================================
    # AUTO REFRESH
    # ==================================================

    def start_auto_refresh(self):

        from PyQt5.QtCore import QTimer

        self.refresh_timer = QTimer()

        self.refresh_timer.timeout.connect(
            self.periodic_refresh
        )

        self.refresh_timer.start(
            3000
        )

    # ==================================================
    # PERIODIC REFRESH
    # ==================================================

    def periodic_refresh(self):

        self.refresh_dashboard()
        self.load_logs()

    # ==================================================
    # ALERT POPUP
    # ==================================================

    def show_alert(
        self,
        title,
        message
    ):

        alert = QMessageBox(self)

        alert.setWindowTitle(title)

        alert.setText(message)

        alert.setIcon(
            QMessageBox.Warning
        )

        alert.exec_()

    # ==================================================
    # MANUAL TABLE REFRESH
    # ==================================================

    def refresh_table(self):

        self.populate_table()
        self.refresh_dashboard()

    # ==================================================
    # EXPORT LOGS
    # ==================================================

    def export_logs(self):

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Logs",
            "activity_logs.txt",
            "Text Files (*.txt)"
        )

        if not save_path:
            return

        try:

            with open(
                "data/activity.log",
                "r",
                encoding="utf-8"
            ) as src:

                content = src.read()

            with open(
                save_path,
                "w",
                encoding="utf-8"
            ) as dst:

                dst.write(content)

            QMessageBox.information(
                self,
                "Export Complete",
                f"Logs saved to:\n{save_path}"
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Error",
                str(e)
            )

    # ==================================================
    # CLEAR LOG VIEW
    # ==================================================

    def clear_log_view(self):

        self.log_viewer.clear()

    # ==================================================
    # WINDOW SHOW EVENT
    # ==================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.refresh_dashboard()
        self.load_logs()

    # ==================================================
    # WINDOW CLOSE EVENT
    # ==================================================

    def handle_file_modified(self, path):

        self.update_status_message(
            f"Modified: {path}"
        )


    def handle_file_deleted(self, path):

        self.update_status_message(
            f"Deleted: {path}"
        )


    def handle_file_restored(self, path):

        self.update_status_message(
            f"Restored: {path}"
        )

    def closeEvent(self, event):

        reply = QMessageBox.question(
            self,
            "Exit CyberSentinel",
            "Stop monitoring and exit?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            try:

                self.stop_monitoring()

                if hasattr(
                    self,
                    "refresh_timer"
                ):
                    self.refresh_timer.stop()

            except Exception:
                pass

            event.accept()

        else:

            event.ignore()

    # ==================================================
    # INITIALIZE SERVICES
    # ==================================================

    def initialize_services(self):

        self.populate_table()

        self.load_logs()

        self.refresh_dashboard()

        self.start_auto_refresh()

    # ==================================================
    # DASHBOARD QUICK ACTIONS
    # ==================================================

    def dashboard_verify(self):

        self.verify_integrity()

    def dashboard_add_file(self):

        self.browse_file()

    def dashboard_remove(self):

        self.remove_selected_file()

    # ==================================================
    # STATUS BAR UPDATE
    # ==================================================

    def update_status_message(
        self,
        message
    ):

        self.operations_status.setText(
            message
        )

    # ==================================================
    # FILE DETAILS
    # ==================================================

    def get_selected_file(self):

        row = self.files_table.currentRow()

        if row < 0:
            return None

        item = self.files_table.item(
            row,
            1
        )

        if item:
            return item.text()

        return None