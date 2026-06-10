import sys
import hashlib
import base64
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame)
from PySide6.QtCore import Qt

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

STYLE_SHEET = """
QMainWindow { background-color: #0F111A; }
QWidget { color: #E0E0E0; font-family: 'Segoe UI'; }
QFrame#Card { background-color: #1A1C26; border-radius: 12px; border: 1px solid #2D2F3F; padding: 20px; }
QLabel#Title { font-size: 20px; font-weight: bold; color: #00F0FF; margin-bottom: 15px; }
QLineEdit { background-color: #0F111A; border: 1px solid #3D3F4F; border-radius: 6px; padding: 10px; color: white; font-size: 14px; }
QLineEdit:focus { border: 1px solid #00F0FF; }
QPushButton { background-color: #00F0FF; color: #0F111A; border-radius: 6px; padding: 12px; font-weight: bold; }
QPushButton:hover { background-color: #00D0DD; }
QPushButton#EyeBtn { background-color: transparent; border: none; color: #5D5F6F; font-size: 18px; }
QTableWidget { background-color: #1A1C26; border: none; gridline-color: #2D2F3F; margin-top: 15px; }
QHeaderView::section { background-color: #242735; color: #00F0FF; padding: 8px; border: none; font-weight: bold; }
"""

class RunnerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VAULT ACCESS")
        self.setFixedSize(600, 500)
        self.setStyleSheet(STYLE_SHEET)
        self.load_data()
        self.init_ui()

    def load_data(self):
        try:
            with open(resource_path('vault_data.json'), 'r') as f:
                d = json.load(f)
                self.list_of_encrypted = d['list_of_encrypted']
                self.chunk_num = d['chunk_num']
                self.keys_index = d['keys_index']
                self.values_index = d['values_index']
        except: sys.exit()

    def init_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        self.card = QFrame(); self.card.setObjectName("Card")
        c_lay = QVBoxLayout(self.card)
        
        title = QLabel("SECURE AUTHORIZATION"); title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter); c_lay.addWidget(title)
        
        h_lay = QHBoxLayout()
        self.m_in = QLineEdit(); self.m_in.setPlaceholderText("Enter Master Password")
        self.m_in.setEchoMode(QLineEdit.Password)
        self.m_in.returnPressed.connect(self.unlock)
        
        self.eye_btn = QPushButton("👁")
        self.eye_btn.setObjectName("EyeBtn"); self.eye_btn.setCheckable(True)
        self.eye_btn.clicked.connect(lambda: self.m_in.setEchoMode(QLineEdit.Normal if self.eye_btn.isChecked() else QLineEdit.Password))
        
        h_lay.addWidget(self.m_in); h_lay.addWidget(self.eye_btn)
        c_lay.addLayout(h_lay)
        
        btn = QPushButton("UNLOCK")
        btn.clicked.connect(self.unlock)
        c_lay.addWidget(btn)
        layout.addWidget(self.card)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Username", "Password"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

    def unlock(self):
        pwd = self.m_in.text()
        try:
            # Reconstruct logic from setup
            master_chars = [str(c) for c in pwd]
            input_to_hash = []
            for num in self.chunk_num:
                input_to_hash.append(master_chars[:num])
                del master_chars[:num]

            hash_lit = []
            idx = 0
            for chunk in input_to_hash:
                h_val = ""
                for char in chunk:
                    h_val += str(self.list_of_encrypted[idx].get(char))
                    idx += 1
                a = hashlib.sha512(h_val.encode()).digest()
                hash_lit.append(base64.b85encode(a).decode())

            self.table.setRowCount(0)
            for k_idx, v_idx in zip(self.keys_index, self.values_index):
                u = "".join([hash_lit[h][p] for p, h in k_idx])
                p = "".join([hash_lit[h][p] for p, h in v_idx])
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(u))
                self.table.setItem(row, 1, QTableWidgetItem(p))
            
            self.card.setStyleSheet("QFrame#Card { border: 1px solid #00FF41; }")
        except:
            self.card.setStyleSheet("QFrame#Card { border: 1px solid #FF5555; }")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RunnerGUI(); window.show()
    sys.exit(app.exec())
