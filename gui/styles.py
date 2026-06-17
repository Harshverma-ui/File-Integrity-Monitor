CYBER_STYLE = """
/* =====================================================
   MAIN WINDOW
===================================================== */

QMainWindow {
    background-color: #0B1020;
}

QWidget {
    color: white;
    font-family: Segoe UI;
    font-size: 12px;
}


/* =====================================================
   SIDEBAR
===================================================== */

#sidebar {
    background-color: rgba(10,15,30,220);
    border-right: 1px solid rgba(0,212,255,60);
    border-radius: 15px;
}

QPushButton#navButton {
    background-color: transparent;
    text-align: left;
    padding: 12px;
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 13px;
}

QPushButton#navButton:hover {
    background-color: rgba(0,212,255,40);
    border-left: 4px solid #00D4FF;
}

QPushButton#navButton:pressed {
    background-color: rgba(0,212,255,80);
}


/* =====================================================
   TITLE BAR
===================================================== */

#titleBar {
    background-color: rgba(18,25,45,220);
    border-radius: 15px;
}

#titleLabel {
    font-size: 24px;
    font-weight: bold;
    color: #00D4FF;
}


/* =====================================================
   DASHBOARD CARDS
===================================================== */

#card {
    background-color: #111827;
    border: 2px solid #00D4FF;
    border-radius: 15px;
    padding: 15px;
}



#cardTitle {
    font-size: 14px;
    color: #A0AEC0;
    font-weight: 500;
}

#cardValue {
    font-size: 28px;
    font-weight: bold;
    color: #E5E7EB;
}


/* =====================================================
   STATUS COLORS
===================================================== */

#safeCard {
    background-color: rgba(0,255,153,30);
    border: 1px solid rgba(0,255,153,120);
    border-radius: 20px;
}

#modifiedCard {
    background-color: rgba(255,77,77,30);
    border: 1px solid rgba(255,77,77,120);
    border-radius: 20px;
}

#monitorCard {
    background-color: rgba(0,212,255,25);
    border: 1px solid rgba(0,212,255,120);
    border-radius: 20px;
}


/* =====================================================
   BUTTONS
===================================================== */

QPushButton {
    background-color: #00D4FF;
    border: none;
    border-radius: 12px;
    padding: 10px;
    color: black;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #00F5FF;
}

QPushButton:pressed {
    background-color: #00A8CC;
}


/* =====================================================
   ACTION BUTTONS
===================================================== */

#actionButton {
    background-color: rgba(0,212,255,25);
    color: white;
    border: 1px solid rgba(0,212,255,100);
    border-radius: 12px;
    padding: 12px;
}

#actionButton:hover {
    background-color: rgba(0,212,255,60);
    border: 1px solid #00D4FF;
}

#actionButton:pressed {
    background-color: rgba(0,212,255,100);
}


/* =====================================================
   TABLES
===================================================== */

QTableWidget {
    background-color: rgba(20,30,50,190);
    border: 1px solid rgba(0,212,255,70);
    border-radius: 15px;
    gridline-color: rgba(255,255,255,20);
}

QHeaderView::section {
    background-color: #16324F;
    color: #00D4FF;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: rgba(0,212,255,90);
}


/* =====================================================
   LOG VIEWER
===================================================== */

QTextEdit {
    background-color: rgba(20,30,50,190);
    border: 1px solid rgba(0,212,255,70);
    border-radius: 15px;
    color: #00FF99;
    padding: 10px;
    font-family: Consolas;
}


/* =====================================================
   SEARCH BOX
===================================================== */

QLineEdit {
    background-color: rgba(20,30,50,190);
    border: 1px solid rgba(0,212,255,70);
    border-radius: 12px;
    padding: 8px;
    color: white;
}

QLineEdit:focus {
    border: 1px solid #00D4FF;
}


/* =====================================================
   COMBOBOX
===================================================== */

QComboBox {
    background-color: rgba(20,30,50,190);
    border: 1px solid rgba(0,212,255,70);
    border-radius: 12px;
    padding: 6px;
    color: white;
}


/* =====================================================
   SCROLLBAR
===================================================== */

QScrollBar:vertical {
    background: transparent;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: rgba(0,212,255,120);
    border-radius: 6px;
}

QScrollBar::handle:vertical:hover {
    background: #00D4FF;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 12px;
}

QScrollBar::handle:horizontal {
    background: rgba(0,212,255,120);
    border-radius: 6px;
}


/* =====================================================
   MESSAGE BOX
===================================================== */

QMessageBox {
    background-color: #101826;
}

QMessageBox QLabel {
    color: white;
}


/* =====================================================
   STATUS LABELS
===================================================== */

#safeLabel {
    color: #00FF99;
    font-weight: bold;
}

#modifiedLabel {
    color: #FF4D4D;
    font-weight: bold;
}

#missingLabel {
    color: #FFA500;
    font-weight: bold;
}


/* =====================================================
   LOGO AREA
===================================================== */

#logoContainer {
    background-color: transparent;
}

#logoText {
    color: #00D4FF;
    font-size: 18px;
    font-weight: bold;
}


/* =====================================================
   REAL-TIME MONITOR INDICATOR
===================================================== */

#monitorStatus {
    color: #00FF99;
    font-weight: bold;
    font-size: 14px;
}


/* =====================================================
   TOOLTIP
===================================================== */

QToolTip {
    background-color: #00D4FF;
    color: black;
    border: none;
    padding: 5px;
}

QTableWidget {
    border-radius: 15px;
    background-color: #0F172A;
    selection-background-color: #00D4FF;
}

QTableCornerButton::section {
    background-color: #16324F;
    border: none;
}
"""
