"""
MAC 修改核心模块
阶段3

Windows实现方式：
- 通过 NDIS 注册表 NetworkAddress 覆盖 MAC
- 不修改物理固件地址
- 支持重新加载网卡配置
"""

import os
import subprocess
import winreg


class MacModifier:
    def __init__(self):
        self.supported = os.name == "nt"

    def validate_mac(self, mac: str) -> str:
        """标准化 MAC 地址"""
        value = mac.replace(":", "").replace("-", "").upper()

        if len(value) != 12:
            raise ValueError("MAC地址长度错误")

        if not all(c in "0123456789ABCDEF" for c in value):
            raise ValueError("MAC地址格式错误")

        return value

    def set_registry_mac(self, adapter_guid: str, mac: str):
        """
        写入 NDIS NetworkAddress

        adapter_guid 示例:
        {XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
        """

        if not self.supported:
            raise RuntimeError("当前系统不是Windows")

        mac = self.validate_mac(mac)

        path = (
            r"SYSTEM\\CurrentControlSet\\Control\\Class\\"
            r"{4d36e972-e325-11ce-bfc1-08002be10318}\\"
            f"{adapter_guid}"
        )

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

    def refresh_adapter(self, interface_name: str):
        """
        刷新网卡配置
        后续阶段接入更精准PNP控制
        """

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
