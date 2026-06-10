import sys
import hashlib
import base64
import json
import subprocess
import os
import string
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QTableWidget, QTableWidgetItem, QHeaderView, 
                             QStackedWidget, QTextEdit, QProgressBar, QFrame)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon

# --- Core Logic Functions (بدون تغییر در منطق ریاضی شما) ---
def hash_finder_logic(listkey, listval):
    keys = []
    for i in listkey:
        keys.append(i + (str(keys[0]) if keys else "0"))
    vals = []
    for i in listval:
        vals.append(i + (str(vals[0]) if vals else "0"))
    item = (keys[0] if keys else "") + (vals[0] if vals else "")
    key_list_of_dic = {i for i in item}
    check = False
    hash_nums_map = []
    if not key_list_of_dic: return []
    for num_part in range(1, len(list(key_list_of_dic))+1):
        if check: break
        if len(list(key_list_of_dic)) % num_part == 0:
            part_size = len(list(key_list_of_dic)) // num_part
            chunk = [set(list(key_list_of_dic)[i:i+part_size]) for i in range(0, len(list(key_list_of_dic)), part_size)]
            for n in range(len(chunk)):
                for s in range(100, 10000):
                    b85 = base64.b85encode(hashlib.sha512(str(s).encode()).digest()).decode()
                    if all(c in b85 for c in chunk[n]):
                        hash_nums_map.append(s)
                        check = True
                        break
    return list(set(hash_nums_map))

def mapping_logic(hash_num_maps, master_password, hash_length):
    new_master_pass = [str(i) for i in master_password]
    new_master_pass = new_master_pass[:hash_length]
    list_of_tables = []
    all_chars = string.ascii_letters + string.digits + string.punctuation
    
    for number in range(len(hash_num_maps)):
        for hass, maspas in zip(str(hash_num_maps[number]), new_master_pass.copy()):
            randomize_cache = {maspas: hass}
            if maspas in new_master_pass: new_master_pass.remove(maspas)
            while len(randomize_cache) < 20:
                key = random.choice(all_chars)
                if key not in randomize_cache:
                    randomize_cache[key] = random.randint(0, 9)
            items = list(randomize_cache.items())
            random.shuffle(items)
            list_of_tables.append(dict(items))
    return list_of_tables

# --- GUI Styles ---
STYLE_SHEET = """
QMainWindow { background-color: #0F111A; }
QWidget { color: #E0E0E0; font-family: 'Segoe UI'; }
QFrame#Card { background-color: #1A1C26; border-radius: 12px; border: 1px solid #2D2F3F; }
QLabel#Title { font-size: 20px; font-weight: bold; color: #00F0FF; }
QLineEdit { background-color: #0F111A; border: 1px solid #3D3F4F; border-radius: 6px; padding: 8px; color: white; }
QLineEdit:focus { border: 1px solid #00F0FF; }
QPushButton { background-color: #00F0FF; color: #0F111A; border-radius: 6px; padding: 10px; font-weight: bold; }
QPushButton:hover { background-color: #00D0DD; }
QPushButton#Secondary { background-color: transparent; border: 1px solid #00F0FF; color: #00F0FF; }
QPushButton#EyeBtn { background-color: transparent; border: none; color: #5D5F6F; font-size: 18px; }
QTableWidget { background-color: #1A1C26; border: none; gridline-color: #2D2F3F; }
QTextEdit#Console { background-color: #050505; color: #00FF41; font-family: 'Consolas'; border-radius: 8px; }
"""

class Worker(QThread):
    log_signal = Signal(str)
    finished_signal = Signal(str)

    def __init__(self, user_pass_dic, master_pass):
        super().__init__()
        self.user_pass_dic = user_pass_dic
        self.master_pass = master_pass

    def run(self):
        try:
            self.log_signal.emit("[⚡] Initializing Security Layer...")
            lol = hash_finder_logic(self.user_pass_dic.keys(), self.user_pass_dic.values())
            pass_check_str = "".join(map(str, lol))
            
            list_of_encrypted = mapping_logic(lol, self.master_pass, len(pass_check_str))
            
            chunk_num = [len(str(code)) for code in lol]
            
            # Reconstruction for hashing logic (same as runner)
            master_input = [str(d) for d in self.master_pass]
            temp_input = master_input.copy()
            input_to_hash_list = []
            for num in chunk_num:
                input_to_hash_list.append(temp_input[:num])
                del temp_input[:num]
            
            hash_lit = []
            i_hl = 0
            for chunk in input_to_hash_list:
                gen_h = ""
                for char in chunk:
                    gen_h += str(list_of_encrypted[i_hl].get(char))
                    i_hl += 1
                a = hashlib.sha512(gen_h.encode()).digest()
                hash_lit.append(base64.b85encode(a).decode())

            hash_dic = {h: i for i, h in enumerate(hash_lit)}
            
            def get_indices(data_dict):
                results = []
                for val in data_dict:
                    entry = []
                    for char in val:
                        for idx, h_str in enumerate(hash_lit):
                            pos = h_str.find(char)
                            if pos != -1:
                                entry.append((pos, hash_dic.get(h_str)))
                                break
                    results.append(entry)
                return results

            keys_index = get_indices(self.user_pass_dic.keys())
            values_index = get_indices(self.user_pass_dic.values())

            vault_data = {
                "list_of_encrypted": list_of_encrypted,
                "chunk_num": chunk_num,
                "keys_index": keys_index,
                "values_index": values_index
            }

            with open('vault_data.json', 'w') as f:
                json.dump(vault_data, f)
            
            self.log_signal.emit("[⚙] Compiling Modern Runner (No Console)...")
            
            # --windowed removes the black terminal!
            subprocess.run([
                "pyinstaller", "--noconfirm", "--onefile", "--windowed",
                "--add-data", f"vault_data.json{os.pathsep}.", "runner_gui.py"
            ], capture_output=True)
            
            if os.path.exists('vault_data.json'): os.remove('vault_data.json')
            self.finished_signal.emit("SUCCESS")
        except Exception as e:
            self.log_signal.emit(f"[❌] Error: {str(e)}")
            self.finished_signal.emit("FAILED")

class SetupGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TECH-VAULT SETUP")
        self.resize(800, 550)
        self.setStyleSheet(STYLE_SHEET)
        self.user_pass_dic = {}
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_step1())
        self.stack.addWidget(self.create_step2())
        self.stack.addWidget(self.create_step3())
        layout = QVBoxLayout(central)
        layout.addWidget(self.stack)

    def create_step1(self):
        frame = QFrame(); frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        title = QLabel("ENTRY MANAGEMENT"); title.setObjectName("Title")
        layout.addWidget(title)
        
        h_lay = QHBoxLayout()
        self.u_in = QLineEdit(); self.u_in.setPlaceholderText("Username")
        self.p_in = QLineEdit(); self.p_in.setPlaceholderText("Password")
        self.p_in.setEchoMode(QLineEdit.Password)
        
        self.eye_btn = QPushButton("👁")
        self.eye_btn.setObjectName("EyeBtn")
        self.eye_btn.setCheckable(True)
        self.eye_btn.clicked.connect(lambda: self.p_in.setEchoMode(QLineEdit.Normal if self.eye_btn.isChecked() else QLineEdit.Password))
        
        add_btn = QPushButton("ADD")
        add_btn.clicked.connect(self.add_data)
        
        h_lay.addWidget(self.u_in); h_lay.addWidget(self.p_in); h_lay.addWidget(self.eye_btn); h_lay.addWidget(add_btn)
        layout.addLayout(h_lay)
        
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["User", "Pass"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        
        next_btn = QPushButton("CONTINUE")
        next_btn.clicked.connect(self.go_to_step2)
        layout.addWidget(next_btn)
        return frame

    def create_step2(self):
        frame = QFrame(); frame.setObjectName("Card")
        layout = QVBoxLayout(frame); layout.setAlignment(Qt.AlignCenter)
        title = QLabel("MASTER SECURITY"); title.setObjectName("Title")
        layout.addWidget(title, 0, Qt.AlignCenter)
        
        self.info_lbl = QLabel("Enter your master key")
        layout.addWidget(self.info_lbl, 0, Qt.AlignCenter)
        
        self.m_pass = QLineEdit(); self.m_pass.setEchoMode(QLineEdit.Password)
        self.m_pass.setFixedWidth(300)
        layout.addWidget(self.m_pass, 0, Qt.AlignCenter)
        
        run_btn = QPushButton("GENERATE SECURE EXE")
        run_btn.clicked.connect(self.start_work)
        layout.addWidget(run_btn, 0, Qt.AlignCenter)
        return frame

    def create_step3(self):
        frame = QFrame(); frame.setObjectName("Card")
        layout = QVBoxLayout(frame)
        self.console = QTextEdit(); self.console.setObjectName("Console"); self.console.setReadOnly(True)
        layout.addWidget(self.console)
        self.pbar = QProgressBar(); self.pbar.setRange(0, 0)
        layout.addWidget(self.pbar)
        return frame

    def add_data(self):
        u, p = self.u_in.text(), self.p_in.text()
        if u and p:
            self.user_pass_dic[u] = p
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(u))
            self.table.setItem(row, 1, QTableWidgetItem("●●●●"))
            self.u_in.clear(); self.p_in.clear()

    def go_to_step2(self):
        if self.user_pass_dic:
            self.stack.setCurrentIndex(1)

    def start_work(self):
        self.stack.setCurrentIndex(2)
        self.worker = Worker(self.user_pass_dic, self.m_pass.text())
        self.worker.log_signal.connect(self.console.append)
        self.worker.finished_signal.connect(lambda: [self.pbar.setRange(0, 100), self.pbar.setValue(100)])
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SetupGUI(); window.show()
    sys.exit(app.exec())
