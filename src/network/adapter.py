"""
Network adapter information provider.

Stage 2 foundation module.
Only responsible for reading adapter information.
MAC modification logic will be integrated later.
"""

import platform


def get_adapters():
    """Return network adapter information list.

    Current implementation is intentionally conservative so later
    Windows-specific providers can be added without changing GUI code.
    """
    adapters = []

    try:
        import psutil

        stats = psutil.net_if_stats()
        addresses = psutil.net_if_addrs()

        for name, addr_list in addresses.items():
            mac = ""
            for addr in addr_list:
                if getattr(addr, "family", None) == getattr(psutil, "AF_LINK", object()):
                    mac = addr.address

            adapters.append({
                "name": name,
                "mac": mac,
                "status": "启用" if stats.get(name) and stats[name].isup else "禁用",
                "description": "",
                "system": platform.system(),
            })
    except Exception:
        pass

    return adapters
