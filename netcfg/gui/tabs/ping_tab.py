import tkinter as tk
from tkinter import ttk, messagebox
import threading
from commands.ping import Pinger


class PingTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._build_ui()

    def _build_ui(self):
        # Label en entry voor host/IP
        ttk.Label(self, text="Host/IP:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_host = ttk.Entry(self, width=30)
        self.entry_host.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.entry_host.insert(0, "8.8.8.8")

        # Label en entry voor aantal pings
        ttk.Label(self, text="Aantal (pakketten):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_count = ttk.Entry(self, width=10)
        self.entry_count.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.entry_count.insert(0, "4")

        # Frame voor knoppen en checkbox
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5, padx=5)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Ping uitvoeren knop
        ttk.Button(button_frame, text="Ping uitvoeren", command=self.run_ping).grid(row=0, column=0, padx=5, sticky="ew")
        # Checkbox voor infinite ping
        self.var_infinite = tk.BooleanVar()
        tk.Checkbutton(button_frame, text="Oneindig pingen (-t)", variable=self.var_infinite).grid(row=0, column=1, padx=5, sticky="w")
        # Stop knop
        ttk.Button(button_frame, text="Stop Ping", command=self.stop_ping).grid(row=0, column=2, padx=5, sticky="ew")

        # Text widget voor output
        self.text_output = tk.Text(self, height=15, wrap="word")
        self.text_output.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Maak laatste rij en kolom stretchable
        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)







    def run_ping(self):
        host = self.entry_host.get().strip()
        if not host:
            messagebox.showerror("Fout", "Voer een host of IP in.")
            return

        try:
            count = int(self.entry_count.get().strip())
        except ValueError:
            count = 4

        infinite = self.var_infinite.get()  # bijvoorbeeld gekoppeld aan een checkbox

        # Maak het tekstvak leeg
        self.text_output.delete("1.0", tk.END)

        # Maak een nieuwe Pinger aan
        self.pinger = Pinger(host=host, count=count, infinite=infinite)

        def worker():
            for line in self.pinger.run():
                # Regels veilig toevoegen aan GUI via main-thread
                self.after(0, lambda l=line: self.text_output.insert(tk.END, l + "\n"))
                self.after(0, lambda: self.text_output.see(tk.END))

        # Start ping in aparte thread
        threading.Thread(target=worker, daemon=True).start()


    def stop_ping(self):
        if hasattr(self, "pinger") and self.pinger:
            self.pinger.stop()
            self.text_output.insert(tk.END, "\nPing gestopt door gebruiker.\n")
            self.text_output.see(tk.END)