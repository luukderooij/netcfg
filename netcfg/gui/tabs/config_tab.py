import tkinter as tk
from tkinter import ttk, messagebox
import threading
from netcfg import core, settings


class ConfigTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.adapter_var = tk.StringVar()
        self._build_ui()
        self.start_auto_refresh()

    def _build_ui(self):
        ttk.Label(self, text="Kies netwerkadapter:").pack(anchor="w")
        adapters = core.list_adapters()
        combo = ttk.Combobox(
            self, 
            textvariable=self.adapter_var, 
            values=adapters, 
            state="readonly"
        )
        combo.pack(fill="x", pady=5)

        # als er eerder een adapter was opgeslagen → selecteer die alvast
        last = settings.get("last_adapter")
        if last in adapters:
            self.adapter_var.set(last)

        # event: opslaan wanneer gebruiker een nieuwe kiest
        combo.bind("<<ComboboxSelected>>", self._on_adapter_selected)

        self.text = tk.Text(self, height=15, wrap="word")
        self.text.pack(fill="both", expand=True)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="DHCP → Statisch", command=self.action_set_static).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Terug naar DHCP", command=self.action_set_dhcp).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Config opnieuw tonen", command=self.refresh_config).pack(side="left", padx=5)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", pady=5)
        self.progress.pack_forget()

    def refresh_config(self):
        adapter = self.adapter_var.get()
        if not adapter:
            return
        config = core.get_adapter_config(adapter)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, f"🔎 Configuratie voor {adapter}:\n")
        self.text.insert(tk.END, f"   IP-adres : {config['ip'] or 'onbekend'}\n")
        self.text.insert(tk.END, f"   Subnet   : {config['mask'] or 'onbekend'}\n")
        self.text.insert(tk.END, f"   Gateway  : {config['gateway'] or 'onbekend'}\n")
        self.text.insert(tk.END, f"   DNS      : {', '.join(config['dns']) if config['dns'] else 'geen'}\n")
        return config

    def action_set_static(self):
        adapter = self.adapter_var.get()
        if not adapter:
            return

        def worker():
            try:
                core.set_static(adapter, self.refresh_config())
                self.after(0, lambda: messagebox.showinfo("Succes", f"✅ {adapter} ingesteld op statisch."))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Fout", str(e)))
            finally:
                self.after(0, self.finish_action)

        self.start_action()
        threading.Thread(target=worker, daemon=True).start()

    def action_set_dhcp(self):
        adapter = self.adapter_var.get()
        if not adapter:
            return

        def worker():
            try:
                core.set_dhcp(adapter)
                self.after(0, lambda: messagebox.showinfo("Succes", f"✅ {adapter} teruggezet naar DHCP."))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Fout", str(e)))
            finally:
                self.after(0, self.finish_action)

        self.start_action()
        threading.Thread(target=worker, daemon=True).start()

    def start_action(self):
        self.progress.pack(fill="x", pady=5)
        self.progress.start(10)

    def finish_action(self):
        self.progress.stop()
        self.progress.pack_forget()


    def start_auto_refresh(self, interval=2000):
        """Start periodieke refresh (default elke 2 sec)."""
        self._auto_refresh = True
        self._refresh_loop(interval)

    def stop_auto_refresh(self):
        """Stop de automatische refresh."""
        self._auto_refresh = False

    def _refresh_loop(self, interval):
        if self._auto_refresh:
            self.refresh_config()
            self.after(interval, lambda: self._refresh_loop(interval))

    def _on_adapter_selected(self, event=None):
        adapter = self.adapter_var.get()
        if adapter:
            settings.set("last_adapter", adapter)
            settings.save_settings()