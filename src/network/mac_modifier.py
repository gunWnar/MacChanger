"""
网卡管理工具 v1.0
MAC 修改核心模块
阶段3完善版

功能：
- NDIS NetworkAddress 修改
- 自动定位网卡注册表项
- 支持恢复默认MAC覆盖
- 支持刷新网卡
"""

import os
import re
import subprocess
import winreg


NDIS_PATH = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"


class MacModifier:
    def __init__(self):
        self.supported = os.name == "nt"

    def validate_mac(self, mac: str) -> str:
        value = re.sub(r"[^0-9A-Fa-f]", "", mac)
        if len(value) != 12:
            raise ValueError("MAC地址格式错误")
        return value.upper()

    def find_adapter_slot(self, adapter_guid: str):
        """根据网卡GUID定位NDIS配置编号"""
        if not self.supported:
            raise RuntimeError("仅支持Windows")

        root = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            NDIS_PATH,
        )

        index = 0
        while True:
            try:
                name = winreg.EnumKey(root, index)
                key = winreg.OpenKey(root, name)
                try:
                    guid, _ = winreg.QueryValueEx(key, "NetCfgInstanceId")
                    if guid.lower() == adapter_guid.lower():
                        return name
                except FileNotFoundError:
                    pass
                index += 1
            except OSError:
                break

        return None

    def change_mac(self, adapter_guid: str, new_mac: str):
        """修改MAC覆盖值"""
        if not self.supported:
            raise RuntimeError("当前系统不是Windows")

        mac = self.validate_mac(new_mac)
        slot = self.find_adapter_slot(adapter_guid)

        if not slot:
            raise RuntimeError("找不到网卡配置")

        path = NDIS_PATH + "\\" + slot
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            path,
            0,
            winreg.KEY_SET_VALUE,
        )

        winreg.SetValueEx(
            key,
            "NetworkAddress",
            0,
            winreg.REG_SZ,
            mac,
        )

        winreg.CloseKey(key)
        return True

    def restore_mac(self, adapter_guid: str):
        """删除覆盖恢复默认MAC"""
        slot = self.find_adapter_slot(adapter_guid)
        if not slot:
            return False

        path = NDIS_PATH + "\\" + slot
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            path,
            0,
            winreg.KEY_SET_VALUE,
        )

        try:
            winreg.DeleteValue(key, "NetworkAddress")
        except FileNotFoundError:
            pass

        winreg.CloseKey(key)
        return True

    def refresh_adapter(self, interface_name: str):
        if not self.supported:
            return False

        subprocess.run(
            [
                "powershell",
                "-Command",
                f"Restart-NetAdapter -Name '{interface_name}' -Confirm:$false",
            ],
            capture_output=True,
        )
        return True
