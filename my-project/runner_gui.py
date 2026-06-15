import sys
import hashlib
import base64
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFrame)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices 

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Styles ---
STYLE_SHEET = """
QMainWindow { background-color: #0F111A; }
QWidget { color: #E0E0E0; font-family: 'Segoe UI'; }
QFrame#Card { background-color: #1A1C26; border-radius: 12px; border: 1px solid #2D2F3F; padding: 20px; }
QLineEdit { background-color: #0F111A; border: 1px solid #3D3F4F; border-radius: 6px; padding: 10px; color: white; }
QPushButton { background-color: #00F0FF; color: #0F111A; border-radius: 6px; padding: 10px; font-weight: bold; }
QPushButton:hover { background-color: #00D0DD; }
QTableWidget { background-color: #1A1C26; border: none; gridline-color: #2D2F3F; }
QHeaderView::section { background-color: #242735; color: #00F0FF; border: none; padding: 5px; font-weight: bold; }
QPushButton#ActionBtn { background-color: #2D2F3F; color: #00F0FF; border: 1px solid #3D3F4F; padding: 5px; min-width: 30px; }
QPushButton#SaveBtn { background-color: #00FF41; color: #000; margin-top: 10px; }
"""

class RunnerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VAULT ACCESS - SECURE")
        self.resize(950, 650)
        self.setStyleSheet(STYLE_SHEET)
        
        self.meta_file = "vault_metadata.json"
        self.load_vault_data()
        self.load_metadata()
        self.init_ui()

    def load_vault_data(self):
        try:
            with open(resource_path('vault_data.json'), 'r') as f:
                d = json.load(f)
                self.list_of_encrypted = d['list_of_encrypted']
                self.chunk_num = d['chunk_num']
                self.keys_index = d['keys_index']
                self.values_index = d['values_index']
        except:
            sys.exit("Critical Error: Vault data not found.")

    def load_metadata(self):
        # Load local labels/links if they exist
        if os.path.exists(self.meta_file):
            with open(self.meta_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def init_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        self.card = QFrame(); self.card.setObjectName("Card")
        c_lay = QVBoxLayout(self.card)
        
        self.m_in = QLineEdit(); self.m_in.setPlaceholderText("Enter Master Password to Decrypt Vault")
        self.m_in.setEchoMode(QLineEdit.Password)
        self.m_in.returnPressed.connect(self.unlock)
        
        btn = QPushButton("UNLOCK AND DECRYPT"); btn.clicked.connect(self.unlock)
        
        c_lay.addWidget(self.m_in); c_lay.addWidget(btn)
        layout.addWidget(self.card)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Label / Site Name", "Website Link", "Username", "Password", "Quick Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        self.save_btn = QPushButton("SAVE ALL LABELS & LINKS")
        self.save_btn.setObjectName("SaveBtn")
        self.save_btn.clicked.connect(self.save_all_metadata)
        self.save_btn.hide()
        layout.addWidget(self.save_btn)

    def unlock(self):
        pwd = self.m_in.text()
        try:
            # --- Your Original Logic ---
            master_chars = [str(c) for c in pwd]
            input_to_hash = []
            for num in self.chunk_num:
                input_to_hash.append(master_chars[:num]); del master_chars[:num]

            hash_lit = []
            idx = 0
            for chunk in input_to_hash:
                h_val = "".join([str(self.list_of_encrypted[idx + i].get(c)) for i, c in enumerate(chunk)])
                idx += len(chunk)
                a = hashlib.sha512(h_val.encode()).digest()
                hash_lit.append(base64.b85encode(a).decode())

            self.table.setRowCount(0)
            for i, (k_idx, v_idx) in enumerate(zip(self.keys_index, self.values_index)):
                u = "".join([hash_lit[h][p] for p, h in k_idx])
                p = "".join([hash_lit[h][p] for p, h in v_idx])
                
                row = self.table.rowCount(); self.table.insertRow(row)
                
                # Metadata key (based on username/index to keep it unique)
                m_key = f"row_{i}"
                saved_label = self.metadata.get(m_key, {}).get('label', "")
                saved_url = self.metadata.get(m_key, {}).get('url', "")

                # Editable Label
                label_in = QLineEdit(saved_label); label_in.setPlaceholderText("e.g. Google")
                self.table.setCellWidget(row, 0, label_in)
                
                # Editable Link
                link_in = QLineEdit(saved_url); link_in.setPlaceholderText("https://...")
                self.table.setCellWidget(row, 1, link_in)

                self.table.setItem(row, 2, QTableWidgetItem(u))
                self.table.setItem(row, 3, QTableWidgetItem(p))
                
                # Actions (Copy & Open Link)
                actions = QWidget(); a_lay = QHBoxLayout(actions); a_lay.setContentsMargins(0,0,0,0)
                
                btn_user = QPushButton("👤"); btn_user.setObjectName("ActionBtn"); btn_user.setToolTip("Copy User")
                btn_user.clicked.connect(lambda ch, s=u: QApplication.clipboard().setText(s))
                
                btn_pass = QPushButton("🔑"); btn_pass.setObjectName("ActionBtn"); btn_pass.setToolTip("Copy Pass")
                btn_pass.clicked.connect(lambda ch, s=p: QApplication.clipboard().setText(s))
                
                btn_go = QPushButton("🌐"); btn_go.setObjectName("ActionBtn"); btn_go.setToolTip("Open URL")
                btn_go.clicked.connect(lambda ch, r=row: self.open_link(r))
                
                a_lay.addWidget(btn_user); a_lay.addWidget(btn_pass); a_lay.addWidget(btn_go)
                self.table.setCellWidget(row, 4, actions)
            
            self.save_btn.show()
            self.card.setStyleSheet("QFrame#Card { border: 1px solid #00FF41; }")
        except:
            self.card.setStyleSheet("QFrame#Card { border: 1px solid #FF5555; }")

    def open_link(self, row):
        link_widget = self.table.cellWidget(row, 1)
        url = link_widget.text()
        if url.startswith("http"):
            QDesktopServices.openUrl(QUrl(url))

    def save_all_metadata(self):
        # Collect data from table and save to local JSON
        new_meta = {}
        for row in range(self.table.rowCount()):
            label = self.table.cellWidget(row, 0).text()
            url = self.table.cellWidget(row, 1).text()
            new_meta[f"row_{row}"] = {"label": label, "url": url}
        
        with open(self.meta_file, 'w') as f:
            json.dump(new_meta, f)
        
        self.metadata = new_meta
        self.save_btn.setText("SAVED SUCCESSFULLY!")
        self.save_btn.setStyleSheet("background-color: #00F0FF;")

if __name__ == "__main__":
    app = QApplication(sys.argv); window = RunnerGUI(); window.show(); sys.exit(app.exec())
