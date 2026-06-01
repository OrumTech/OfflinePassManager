import sys
import hashlib
import base64
import os
import time
import win32clipboard

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QPushButton, QLineEdit, QLabel, QStackedWidget)
from PySide6.QtCore import Qt


def copy_two_passwords(p1, p2):
    combined = f"{p1}\n{p2}"
    clipboard = QApplication.clipboard()
    clipboard.setText(combined)

class PasswordManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Vault")
        self.setFixedSize(350, 450)
        self.entered_password2 = None
        # استایل‌دهی مدرن و جذاب (CSS-like)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #74c7ec;
            }
            QPushButton:pressed {
                background-color: #89dceb;
            }
            QLineEdit {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 8px;
                padding: 10px;
                color: #cdd6f4;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #89b4fa;
            }
        """)

        # لایه اصلی که صفحات مختلف در آن قرار می‌گیرند
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # راه‌اندازی صفحات
        self.init_login_page()
        self.init_dashboard_page()

    def init_login_page(self):
        """طراحی صفحه ورود / تنظیم رمز"""
        login_widget = QWidget()
        layout = QVBoxLayout(login_widget)
        layout.setAlignment(Qt.AlignCenter)

        # عنوان
        title = QLabel("قفل امنیتی")
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 20px; color: #f38ba8;")
        title.setAlignment(Qt.AlignCenter)

        # فیلد رمز عبور
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور خود را وارد کنید...")
        self.password_input.setEchoMode(QLineEdit.Password) # مخفی کردن کاراکترها

        self.password_input2 = QLineEdit()
        self.password_input2.setPlaceholderText("رمز عبور خود را وارد کنید...")
        self.password_input2.setEchoMode(QLineEdit.Password) # مخفی کردن کاراکترها

        # دکمه ورود
        self.btn_login = QPushButton("ورود به برنامه")
        self.btn_login.clicked.connect(self.handle_login)

        layout.addWidget(title)
        layout.addWidget(self.password_input)
        layout.addWidget(self.password_input2)
        layout.addWidget(self.btn_login)

        self.stacked_widget.addWidget(login_widget)

    def init_dashboard_page(self):
        """طراحی صفحه اصلی دارای دکمه سایت‌ها"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        layout.setAlignment(Qt.AlignTop)

        # عنوان داشبورد
        header = QLabel("حساب‌های کاربری شما")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px;")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # لیست سایت‌های نمونه برای تولید دکمه
        sites = [
            {"name": "Google", "id": "google"},
            {"name": "GitHub", "id": "github"},
            {"name": "StackOverflow", "id": "stackoverflow"},
            {"name": "Elearn", "id": "elearn"}
        ]

        # تولید داینامیک دکمه‌ها
        for site in sites:
            btn = QPushButton(f"باز کردن و ورود به {site['name']}")
            # ارسال شناسه سایت به تابع مربوطه هنگام کلیک
            btn.clicked.connect(lambda checked=False, s=site['id']: self.handle_site_click(s))
            layout.addWidget(btn)

        self.stacked_widget.addWidget(dashboard_widget)

    def handle_login(self):
        """
        بک‌اند: در اینجا باید بررسی کنید که آیا فایل هش محلی وجود دارد یا خیر.
        اگر نداشت، این رمز هش و ذخیره شود.
        اگر داشت، هش این ورودی با هش ذخیره شده مقایسه شود.
        """
        entered_password = self.password_input.text()
        self.entered_password2 = self.password_input2.text()
        # کدهای منطقی شما اینجا قرار می‌گیرند
        # فعلا برای تست فرانت‌اند، با وارد کردن هر متنی وارد می‌شویم
        if len(entered_password) > 0:
            print("Authentication Logic Goes Here...")
            self.password_input.clear()
            # انتقال به تب داشبورد
            self.stacked_widget.setCurrentIndex(1)

    def handle_site_click(self, site_id):
        """
        بک‌اند: در این بخش باید مرورگر را باز کنید (مثلا با Selenium یا webbrowser)
        و اطلاعات مربوط به site_id را رمزگشایی کرده و استفاده کنید.
        """
        if site_id == "elearn":

            encoder1 = {0:2, 1:6, 2:5, 3:8, 4:3, 5:6, 6:9, 7:2, 8:1, 9:8}
            encoder2 = {0:5, 1:7, 2:3, 3:6, 4:7, 5:2, 6:8, 7:3, 8:2, 9:4}
            encoder3 = {0:7, 1:4, 2:5, 3:6, 4:8, 5:4, 6:9, 7:2, 8:5, 9:3}
            usersec = [int(d) for d in self.entered_password2]

            chunk1 , chunk2, chunk3 = usersec[:4], usersec[4:8], usersec[8:]
            chunk11 = [encoder1.get(i) for i in chunk1]
            ps1 = str(chunk11[0]) + str(chunk11[1]) + str(chunk11[2]) + str(chunk11[3])
            chunk22 = [encoder2.get(i) for i in chunk2]
            ps2 = str(chunk22[0]) + str(chunk22[1]) + str(chunk22[2]) + str(chunk22[3])
            chunk33 = [encoder3.get(i) for i in chunk3]
            ps3 = str(chunk33[0]) + str(chunk33[1]) + str(chunk33[2])

            hash_sha2 = hashlib.sha256(ps1.encode()).digest()
            hash_b641 = base64.b85encode(hash_sha2).decode()

            hash_sha22 = hashlib.sha256(ps2.encode()).digest()
            hash_b642 = base64.b85encode(hash_sha22).decode()

            hash_sha222 = hashlib.sha256(ps3.encode()).digest()
            hash_b643 = base64.b85encode(hash_sha222).decode()

            elname = hash_b643[20] + hash_b641[31] + hash_b641[20] + hash_b641[33] + hash_b643[20] + hash_b643[20] + hash_b641[33] + hash_b641[34] + "." + hash_b641[31
                ] + hash_b641[19] + hash_b641[5] + hash_b643[20] + hash_b642[23] + hash_b641[0] + hash_b643[13]
            elps = hash_b641[35] + hash_b643[0] + hash_b643[39] + hash_b643[34] + hash_b641[33] + hash_b643[28] + hash_b641[35] + hash_b642[13] + hash_b642[11] + hash_b641[34
                ] + hash_b641[33] + hash_b641[19] + hash_b641[35]
            print(f"your username is: {elname} and pass is {elps}")
            copy_two_passwords(elname,elps)

        print(f"[Backend Action Triggered] Preparing credentials for: {site_id}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManagerApp()
    window.show()
    sys.exit(app.exec())