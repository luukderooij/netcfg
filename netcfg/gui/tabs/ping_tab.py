import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netcfg.commands import ping


class PingTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Host/IP:").grid(row=0, column=0, sticky="w")
        self.entry_host = ttk.Entry(self, width=30)
        self.entry_host.grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(self, text="Aantal (pakketten):").grid(row=1, column=0, sticky="w")
        self.entry_count = ttk.Entry(self, width=10)
        self.entry_count.insert(0, "4")
        self.entry_count.grid(row=1, column=1, sticky="w", padx=5)

        self.text_output = tk.Text(self, height=15, wrap="word")
        self.text_output.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Button(self, text="Ping uitvoeren", command=self.run_ping).grid(
            row=3, column=0, columnspan=2, pady=5
        )

    def run_ping(self):
        host = self.entry_host.get().strip()
        if not host:
            messagebox.showerror("Fout", "Voer een host of IP in.")
            return
        try:
            count = int(self.entry_count.get().strip())
        except ValueError:
            count = 4

        self.text_output.delete("1.0", tk.END)

        def worker():
            for line in ping.stream_ping(host, count):
                self.after(0, lambda l=line: self.text_output.insert(tk.END, l + "\n"))

        threading.Thread(target=worker, daemon=True).start()
