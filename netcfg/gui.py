import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import threading

from . import core
#from .version import __version__
from .changelog import CHANGELOG

import importlib.metadata
import pathlib
import tomllib

source_location = pathlib.Path(__file__).parent
if (source_location.parent / "pyproject.toml").exists():
    with open(source_location.parent / "pyproject.toml", "rb") as f:
        __version__ = tomllib.load(f)['project']['version']
else:
    __version__ = importlib.metadata.version("netcfg")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def launch_gui():
    if not is_admin():
        messagebox.showerror("Administrator vereist", "❌ Start dit programma als administrator.")
        return

    root = tk.Tk()
    root.title("Netwerk Configuratie Tool")
    root.geometry("700x500")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Tab 1: Configuratie
    frame_config = ttk.Frame(notebook, padding=10)
    notebook.add(frame_config, text="Configuratie")

    ttk.Label(frame_config, text="Kies netwerkadapter:").pack(anchor="w")
    adapters = core.list_adapters()
    adapter_var = tk.StringVar()
    combo = ttk.Combobox(frame_config, textvariable=adapter_var, values=adapters, state="readonly")
    combo.pack(fill="x", pady=5)

    text = tk.Text(frame_config, height=15, wrap="word")
    text.pack(fill="both", expand=True)

    def start_action():
        progress.pack(fill="x", pady=5)
        progress.start(10)  # snelheid animatie
        root.update_idletasks()

    def finish_action():
        progress.stop()
        progress.pack_forget()
        refresh_config()

    def refresh_config():
        adapter = adapter_var.get()
        if not adapter:
            return
        config = core.get_adapter_config(adapter)
        text.delete("1.0", tk.END)
        text.insert(tk.END, f"🔎 Configuratie voor {adapter}:\n")
        text.insert(tk.END, f"   IP-adres : {config['ip'] or 'onbekend'}\n")
        text.insert(tk.END, f"   Subnet   : {config['mask'] or 'onbekend'}\n")
        text.insert(tk.END, f"   Gateway  : {config['gateway'] or 'onbekend'}\n")
        text.insert(tk.END, f"   DNS      : {', '.join(config['dns']) if config['dns'] else 'geen'}\n")
        return config

    
    def action_set_static():
        adapter = adapter_var.get()
        if not adapter:
            return

        def worker():
            config = core.get_adapter_config(adapter)
            try:
                core.set_static(adapter, config)
                root.after(0, lambda: messagebox.showinfo("Succes", f"✅ {adapter} ingesteld op statisch."))
            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Fout", str(e)))
            finally:
                root.after(0, finish_action)

        start_action()
        threading.Thread(target=worker, daemon=True).start()

   
    def action_set_dhcp():
        adapter = adapter_var.get()
        if not adapter:
            return

        def worker():
            try:
                core.set_dhcp(adapter)
                root.after(0, lambda: messagebox.showinfo("Succes", f"✅ {adapter} teruggezet naar DHCP."))
            except Exception as e:
                root.after(0, lambda: messagebox.showerror("Fout", str(e)))
            finally:
                root.after(0, finish_action)

        start_action()
        threading.Thread(target=worker, daemon=True).start()

    btn_frame = ttk.Frame(frame_config)
    btn_frame.pack(fill="x", pady=10)

    # Progressbar
    progress = ttk.Progressbar(frame_config, mode="indeterminate")
    progress.pack(fill="x", pady=5)
    progress.pack_forget()  # verberg standaard

    ttk.Button(btn_frame, text="DHCP → Statisch", command=action_set_static).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Terug naar DHCP", command=action_set_dhcp).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Config opnieuw tonen", command=refresh_config).pack(side="left", padx=5)

    # Tab 2: Over / Changelog
    frame_about = ttk.Frame(notebook, padding=10)
    notebook.add(frame_about, text="Over")

    label_version = ttk.Label(frame_about, text=f"Versie: {__version__}", font=("TkDefaultFont", 12, "bold"))
    label_version.pack(anchor="w", pady=5)

    text_changelog = tk.Text(frame_about, height=15, wrap="word")
    text_changelog.pack(fill="both", expand=True)
    # Load changelog from CHANGELOG.md instead of changelog.py
    changelog_path = source_location.parent / "CHANGELOG.md"
    if changelog_path.exists():
        with open(changelog_path, encoding="utf-8") as f:
            changelog_content = f.read()
        text_changelog.insert(tk.END, changelog_content)
    else:
        text_changelog.insert(tk.END, "Geen CHANGELOG.md gevonden.")
        text_changelog.insert(tk.END, f"📌 {version}\n   {desc}\n\n")
    text_changelog.config(state="disabled")

    root.mainloop()
