"""网卡管理工具 v1.0 - Stage4"""

import sys
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from network import NetworkAdapterReader
from network.mac_modifier import MacModifier
from utils.admin import require_admin

APP_NAME = "网卡管理工具 v1.0"


class MacChangerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("900x520")
        self.reader = NetworkAdapterReader()
        self.modifier = MacModifier()
        self.adapters = []
        self.build()

    def build(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=10)
        ttk.Button(bar, text="刷新网卡", command=self.refresh).pack(side="left")
        ttk.Button(bar, text="修改MAC", command=self.change).pack(side="left")
        ttk.Button(bar, text="恢复默认", command=self.restore).pack(side="left")

        self.table = ttk.Treeview(self, columns=("id","description","name","mac","status"), show="headings")
        for c,t in [("id","编号"),("description","网卡描述"),("name","接口名称"),("mac","当前MAC"),("status","状态")]:
            self.table.heading(c,text=t)
            self.table.column(c,width=150)
        self.table.pack(fill="both",expand=True,padx=10,pady=10)

    def refresh(self):
        for i in self.table.get_children():
            self.table.delete(i)
        self.adapters = self.reader.get_adapters()
        for a in self.adapters:
            self.table.insert("","end",values=(a.get("id"),a.get("description"),a.get("name"),a.get("mac"),a.get("status")))

    def selected(self):
        s=self.table.selection()
        return self.adapters[self.table.index(s[0])] if s else None

    def change(self):
        a=self.selected()
        if not a:return
        m=simpledialog.askstring("MAC","输入新的MAC")
        if m:
            self.modifier.set_registry_mac(a.get("guid"),m)
            self.modifier.refresh_adapter(a.get("name"))
            self.refresh()

    def restore(self):
        a=self.selected()
        if a:
            self.modifier.restore_mac(a.get("guid"))
            self.refresh()


if __name__ == "__main__":
    if require_admin():
        sys.exit(0)
    MacChangerApp().mainloop()
