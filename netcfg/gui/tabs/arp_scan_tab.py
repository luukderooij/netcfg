import tkinter as tk
from tkinter import ttk, messagebox
import threading

from netcfg.commands.arp_scanner import ArpScanner, NpcapRequiredError
from mac_vendor_lookup import MacLookup, VendorNotFoundError


class ArpScanTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        # mac-vendor-lookup initialiseren
        self.mac_lookup = MacLookup()
        try:
            self.mac_lookup.load_vendors()  # gebruik lokale cache als aanwezig
        except Exception:
            # als cache niet bestaat, wordt Unknown gebruikt tot update
            pass

        self._build_ui()

    def _build_ui(self):
        # Inputvelden
        ttk.Label(self, text="Netwerk (host/IP/cidr):").grid(row=0, column=0, sticky="w")
        self.entry_host = ttk.Entry(self, width=30)
        self.entry_host.grid(row=0, column=1, sticky="ew", padx=5)
        self.entry_host.insert(0, "192.168.1.0/24")

        # Scan knop
        self.btn_scan = ttk.Button(self, text="Scan", command=self.start_scan_thread)
        self.btn_scan.grid(row=0, column=2, padx=(5, 0))

        # Update OUI knop
        self.btn_update = ttk.Button(self, text="Update OUI-database", command=self.start_update_thread)
        self.btn_update.grid(row=0, column=3, padx=(5, 0))

        # Statuslabel
        self.status_var = tk.StringVar(value="Klaar")
        self.lbl_status = ttk.Label(self, textvariable=self.status_var)
        self.lbl_status.grid(row=1, column=0, columnspan=4, sticky="w", pady=(5, 0))

        # Treeview voor resultaten
        columns = ("ip", "mac", "vendor")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.grid(row=2, column=0, columnspan=4, sticky="nsew", pady=10)

        self.tree.heading("ip", text="IP-adres", command=lambda: self._sort_column("ip", False))
        self.tree.heading("mac", text="MAC-adres", command=lambda: self._sort_column("mac", False))
        self.tree.heading("vendor", text="Leverancier", command=lambda: self._sort_column("vendor", False))

        self.tree.column("ip", width=150, anchor="w")
        self.tree.column("mac", width=150, anchor="w")
        self.tree.column("vendor", width=250, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=4, sticky="ns")

        # Layout
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        # ENTER key start scan
        self.entry_host.bind("<Return>", lambda e: self.start_scan_thread())

    # --- Update OUI database ---
    def start_update_thread(self):
        self.btn_update.config(state="disabled")
        self.status_var.set("Bezig met updaten van OUI-database...")
        threading.Thread(target=self._run_update, daemon=True).start()

    def _run_update(self):
        try:
            self.mac_lookup.update_vendors()
            self.status_var.set("OUI-database succesvol bijgewerkt ✅")
        except Exception as e:
            self.status_var.set("Fout bij updaten OUI-database")
            messagebox.showerror("Fout", f"Bijwerken OUI-database mislukt:\n{e}")
        finally:
            self.btn_update.config(state="normal")

    # --- Scannen ---
    def start_scan_thread(self):
        network = self.entry_host.get().strip()
        if not network:
            messagebox.showwarning("Input vereist", "Voer een netwerk (bv. 192.168.1.0/24) in.")
            return

        self.btn_scan.config(state="disabled")
        self.status_var.set(f"Scannen: {network} ...")

        threading.Thread(target=self._run_scan, args=(network,), daemon=True).start()

    def _run_scan(self, network):
        scanner = ArpScanner(open_on_fail=False)
        try:
            self.after(0, self._clear_tree)
            results = scanner.scan(network, timeout=2)
            self.after(0, lambda: self._insert_results(results))
            self.after(0, lambda: self.status_var.set(f"Scan klaar: {len(results)} hosts gevonden"))
        except NpcapRequiredError:
            def handle_npcap():
                messagebox.showerror("Fout", "Npcap (of ander pcap-backend) is vereist voor ARP-scanning.")
                try:
                    scanner.open_npcap_page()
                except Exception:
                    try:
                        scanner.open_ncap_page()
                    except Exception:
                        pass
            self.after(0, handle_npcap)
            self.after(0, lambda: self.status_var.set("Npcap vereist"))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Scan fout", f"Er is een fout opgetreden:\n{e}"))
            self.after(0, lambda: self.status_var.set("Fout tijdens scan"))
        finally:
            self.after(0, lambda: self.btn_scan.config(state="normal"))

    # --- Helpers ---
    def _clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _insert_results(self, results):
        for row in results:
            ip = row.get("ip") if isinstance(row, dict) else getattr(row, "ip", str(row))
            mac = row.get("mac") if isinstance(row, dict) else getattr(row, "mac", "")
            vendor = "Unknown"
            try:
                vendor = self.mac_lookup.lookup(mac)
            except VendorNotFoundError:
                vendor = "Unknown"
            except Exception:
                vendor = "Error"
            self.tree.insert("", "end", values=(ip, mac, vendor))

    def _sort_column(self, col, reverse):
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("ARP Scan (offline vendor lookup)")
    root.geometry("800x450")
    ArpScanTab(root).pack(fill="both", expand=True)
    root.mainloop()
