from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox
)
import sys

from tablejam.tablejam_app import process_files

'''
TableJam Graphical User Interface.
'''

class TableJamGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TableJam 3.0.0")
        self.setMinimumWidth(500)

        self.origin_path = ""
        self.trans_path = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.origin_label = QLabel("Original SRT: não selecionado")
        self.trans_label = QLabel("Translation SRT: não selecionado")

        btn_origin = QPushButton("Selecionar Original")
        btn_trans = QPushButton("Selecionar Tradução")
        btn_run = QPushButton("Processar")

        btn_origin.clicked.connect(self.select_origin)
        btn_trans.clicked.connect(self.select_translation)
        btn_run.clicked.connect(self.run)

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.origin_label)
        layout.addWidget(btn_origin)
        layout.addWidget(self.trans_label)
        layout.addWidget(btn_trans)
        layout.addWidget(btn_run)
        layout.addWidget(QLabel("Status"))
        layout.addWidget(self.log)

        self.setLayout(layout)

    def select_origin(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Original", "", "SRT (*.srt)")
        if path:
            self.origin_path = path
            self.origin_label.setText(f"Original SRT: {path}")

    def select_translation(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar Tradução", "", "SRT (*.srt)")
        if path:
            self.trans_path = path
            self.trans_label.setText(f"Translation SRT: {path}")

    def run(self):
        if not self.origin_path or not self.trans_path:
            QMessageBox.warning(self, "Erro", "Selecione os dois arquivos.")
            return

        try:
            process_files(self.origin_path, self.trans_path)
            self.log.append("Processamento concluído com sucesso.")
            self.log.append("Arquivo table.csv gerado.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

# ================= MAIN =================
def main():
    app = QApplication(sys.argv)
    window = TableJamGUI()
    window.show()
    sys.exit(app.exec())
