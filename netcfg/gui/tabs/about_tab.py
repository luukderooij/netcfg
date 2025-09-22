import tkinter as tk
from tkinter import ttk
import sys, pathlib
import importlib.metadata
import tomllib
import os


class AboutTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._build_ui()

    def _build_ui(self):
        source_location = pathlib.Path(__file__).resolve().parents[3]
        pyproject_path = source_location / "pyproject.toml"

        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                version = tomllib.load(f)["project"]["version"]
        else:
            version = importlib.metadata.version("netcfg")

        label_version = ttk.Label(self, text=f"Versie: {version}", font=("TkDefaultFont", 12, "bold"))
        label_version.pack(anchor="w", pady=5)

        text_changelog = tk.Text(self, height=15, wrap="word")
        text_changelog.pack(fill="both", expand=True)

        changelog_path = source_location / "CHANGELOG.md"
        if changelog_path.exists():
            with open(changelog_path, encoding="utf-8") as f:
                changelog_content = f.read()
            text_changelog.insert(tk.END, changelog_content)
        else:
            text_changelog.insert(tk.END, "Geen CHANGELOG.md gevonden.")

        text_changelog.config(state="disabled")

