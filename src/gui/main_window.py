from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton

from network.adapter import get_adapters


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("网卡管理工具 Pro")
        self.resize(900, 520)
        self.init_ui()
        self.load_adapters()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        title = QLabel("网卡管理工具 Pro")

        self.refresh_button = QPushButton("刷新网卡")
        self.refresh_button.clicked.connect(self.load_adapters)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels([
            "编号",
            "网卡名称",
            "MAC地址",
            "状态"
        ])

        layout.addWidget(title)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.table)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def load_adapters(self):
        adapters = get_adapters()
        self.table.setRowCount(len(adapters))

        for row, adapter in enumerate(adapters):
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(adapter.get("name", "")))
            self.table.setItem(row, 2, QTableWidgetItem(adapter.get("mac", "")))
            self.table.setItem(row, 3, QTableWidgetItem(adapter.get("status", "")))
