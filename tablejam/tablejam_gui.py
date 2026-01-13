from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
from tablejam.tablejam_app import process_files

'''
TableJam Graphical User Interface.
'''

class TableJamGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableJam 3.0.1")
        self.setMinimumWidth(500)

        self.origin_path = ""
        self.trans_path = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.origin_label = QLabel("Original SRT: not selected")
        self.trans_label = QLabel("Translation SRT: not selected")

        btn_origin = QPushButton("Select Original")
        btn_trans = QPushButton("Select Translation")
        btn_run = QPushButton("Process")

        btn_origin.clicked.connect(self.select_origin)
        btn_trans.clicked.connect(self.select_translation)
        btn_run.clicked.connect(self.run)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        credit_label = QLabel(
            '<a href="https://github.com/Pedro3179">Developed by Leonardo Cerqueira</a>'
        )
        credit_label.setOpenExternalLinks(True)
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit_label.setStyleSheet("color: gray; font-size: 10px;")


        layout.addWidget(self.origin_label)
        layout.addWidget(btn_origin)
        layout.addWidget(self.trans_label)
        layout.addWidget(btn_trans)
        layout.addWidget(btn_run)
        layout.addWidget(QLabel("Status"))
        layout.addWidget(self.log)
        layout.addWidget(credit_label)

        self.setLayout(layout)

    def select_origin(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Original", "", "SRT (*.srt)")
        if path:
            self.origin_path = path
            self.origin_label.setText(f"Original SRT: {path}")

    def select_translation(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Translation", "", "SRT (*.srt)")
        if path:
            self.trans_path = path
            self.trans_label.setText(f"Translation SRT: {path}")

    def run(self):
        if not self.origin_path or not self.trans_path:
            QMessageBox.warning(self, "Error:", "Please select both files.")
            return

        try:
            process_files(self.origin_path, self.trans_path)
            self.log.append("Processing completed successfully!")
            self.log.append("table.csv file generated.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

# ================= MAIN =================
def main():
    app = QApplication(sys.argv)
    icon=QIcon('assets/icon/TJ_256_v2.ico')
    app.setWindowIcon(icon)
    window = TableJamGUI()
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec())
