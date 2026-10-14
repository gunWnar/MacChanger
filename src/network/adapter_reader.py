"""
Windows 网卡读取模块
阶段2

目标：
- Windows 10/11 网卡枚举
- 获取网卡描述
- 获取接口名称
- 获取 MAC 地址
- 获取连接状态

Linux 开发环境可导入，运行功能需要 Windows。
"""

import platform


class NetworkAdapterReader:
    def __init__(self):
        self.adapters = []

    def get_adapters(self):
        if platform.system() != "Windows":
            return []

        try:
            import wmi
            c = wmi.WMI()
            result = []

            for index, adapter in enumerate(c.Win32_NetworkAdapter()):
                mac = adapter.MACAddress or ""
                if not mac:
                    continue

                result.append({
                    "id": index + 1,
                    "description": adapter.Name or "Unknown",
                    "name": adapter.NetConnectionID or "",
                    "mac": mac,
                    "status": adapter.NetConnectionStatus or "Unknown"
                })

            self.adapters = result
            return result

        except Exception:
            return []
