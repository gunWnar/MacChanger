"""
网卡管理工具 v1.0
Python GUI 重构版本
阶段2：接入 Windows 网卡读取
"""

import tkinter as tk
from tkinter import ttk

from network import NetworkAdapterReader

APP_NAME = "网卡管理工具 v1.0"


class MacChangerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("900x520")
        self.resizable(False, False)
        self.reader = NetworkAdapterReader()
        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="刷新网卡", command=self.refresh_adapters).pack(side="left", padx=5)
        ttk.Button(top, text="修改MAC").pack(side="left", padx=5)
        ttk.Button(top, text="恢复默认").pack(side="left", padx=5)

        columns = ("id", "description", "name", "mac", "status")
        self.table = ttk.Treeview(self, columns=columns, show="headings")

        headers = {
            "id": "编号",
            "description": "网卡描述",
            "name": "接口名称",
            "mac": "当前MAC",
            "status": "状态",
        }

        for key, text in headers.items():
            self.table.heading(key, text=text)
            self.table.column(key, width=150)

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.status = ttk.Label(self, text="准备就绪")
        self.status.pack(fill="x", padx=10, pady=5)

    def refresh_adapters(self):
        for item in self.table.get_children():
            self.table.delete(item)

        adapters = self.reader.get_adapters()

        for adapter in adapters:
            self.table.insert("", "end", values=(
                adapter["id"],
                adapter["description"],
                adapter["name"],
                adapter["mac"],
                adapter["status"],
            ))

        self.status.config(text=f"读取到 {len(adapters)} 个网卡")


if __name__ == "__main__":
    app = MacChangerApp()
    app.mainloop()
