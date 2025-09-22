import tkinter as tk
from tkinter import ttk, messagebox
import ctypes

from .tabs.config_tab import ConfigTab
from .tabs.ping_tab import PingTab
from .tabs.about_tab import AboutTab

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
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

    # Tabs toevoegen
    notebook.add(ConfigTab(notebook), text="Configuratie")
    notebook.add(PingTab(notebook), text="Ping")
    notebook.add(AboutTab(notebook), text="Over")

    root.mainloop()
