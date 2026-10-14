"""Windows 管理员权限检测"""

import ctypes
import os
import sys


def is_admin():
    if os.name != "nt":
        return False
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def require_admin():
    """不足管理员权限时重新请求提升，避免循环启动"""
    if os.name != "nt" or is_admin():
        return False

    if "--admin-restart" in sys.argv:
        return False

    params = " ".join(sys.argv[1:] + ["--admin-restart"])
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        1,
    )
    return True
