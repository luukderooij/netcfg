import subprocess
import re
import wmi
import time
import sys

def run_silent(cmd):
    startupinfo = None
    creationflags = 0
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        creationflags = subprocess.CREATE_NO_WINDOW

    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
        startupinfo=startupinfo,
        creationflags=creationflags
    )

def list_adapters():
    try:
        result = run_silent(["netsh", "interface", "ip", "show", "config"])
        output = result.stdout
        return re.findall(r'Configuration for interface \"(.*?)\"', output)
    except subprocess.CalledProcessError:
        return []

def get_dns_servers(adapter):
    try:
        c = wmi.WMI()
        for nic in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if adapter.lower() in nic.Description.lower():
                if nic.DNSServerSearchOrder:
                    return [ip for ip in nic.DNSServerSearchOrder
                            if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip)]
                break
    except:
        pass

    try:
        result = run_silent(["netsh", "interface", "ip", "show", "dns", f"name={adapter}"])
        output = result.stdout
        dns_servers = re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", output)
        return list(dict.fromkeys(dns_servers))
    except subprocess.CalledProcessError:
        return []

    return []

def get_adapter_config(adapter):
    try:
        result = run_silent(["netsh", "interface", "ip", "show", "config", f"name={adapter}"])
        output = result.stdout
        ip_matches = re.findall(r"IP Address:\s+([\d\.]+)", output)
        mask_match = re.search(r"mask\s+([\d\.]+)", output)
        gateway_match = re.search(r"Default Gateway:\s+([\d\.]+)", output)
    except subprocess.CalledProcessError:
        return {"ip": None, "mask": None, "gateway": None, "dns": []}

    return {
        "ip": ip_matches[0] if ip_matches else None,
        "mask": mask_match.group(1) if mask_match else None,
        "gateway": gateway_match.group(1) if gateway_match else None,
        "dns": get_dns_servers(adapter)
    }

def is_ipv4(addr: str) -> bool:
    return re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", addr) is not None

def set_static(adapter, config):
    if not config["ip"] or not config["mask"] or not config["gateway"]:
        raise RuntimeError("Geen volledige DHCP-config gevonden.")

    run_silent([
        "netsh", "interface", "ip", "set", "address",
        f"name={adapter}", "static", config["ip"], config["mask"], config["gateway"]
    ])

    dns_servers = [dns for dns in config["dns"] if is_ipv4(dns)]
    if dns_servers:
        run_silent([
            "netsh", "interface", "ip", "set", "dns",
            f"name={adapter}", "static", dns_servers[0]
        ])
        for i, dns in enumerate(dns_servers[1:], start=2):
            run_silent([
                "netsh", "interface", "ip", "add", "dns",
                f"name={adapter}", dns, f"index={i}"
            ])

    time.sleep(2)

def set_dhcp(adapter):
    run_silent([
        "netsh", "interface", "ip", "set", "address",
        f"name={adapter}", "dhcp"
    ])
    run_silent([
        "netsh", "interface", "ip", "set", "dns",
        f"name={adapter}", "dhcp"
    ])
    time.sleep(2)
