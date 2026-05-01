import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import pkg_resources

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Életvitel Tároló - Telepítő Varázsló")
        self.root.geometry("450x400")
        self.root.resizable(False, False)

        # Szükséges külső könyvtárak listája
        # Mivel SQLite és Hashlib beépített, ide azokat tedd, 
        # amiket később adunk hozzá (pl. pandas, requests, matplotlib)
        self.required_packages = [
            'wheel',
            'setuptools',
            # Ide jöhetnek a projekt specifikus függőségek:
            # 'pandas',
            # 'matplotlib'
        ]
        
        self.status_vars = {}
        self.setup_ui()
        self.check_dependencies()

    def setup_ui(self):
        # Cím
        tk.Label(self.root, text="Rendszerösszetevők ellenőrzése", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Lista keret
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Gombok kerete
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side="bottom", pady=20)

        self.install_btn = tk.Button(btn_frame, text="Telepítés", width=12, command=self.install_packages)
        self.install_btn.pack(side="left", padx=5)

        self.run_btn = tk.Button(btn_frame, text="Indítás", width=12, state="disabled", command=self.start_app)
        self.run_btn.pack(side="left", padx=5)

        self.exit_btn = tk.Button(btn_frame, text="Kilépés", width=12, command=self.root.quit)
        self.exit_btn.pack(side="left", padx=5)

    def check_dependencies(self):
        """Ellenőrzi a csomagokat és frissíti a listát."""
        # Töröljük a régi listát a GUI-ról
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        all_installed = True
        
        # Python verzió ellenőrzése (belső elem példa)
        self.add_status_row("Python környezet", True)

        for pkg in self.required_packages:
            installed = self.is_installed(pkg)
            self.add_status_row(pkg, installed)
            if not installed:
                all_installed = False

        if all_installed:
            self.run_btn.config(state="normal")
            self.install_btn.config(state="disabled")
        else:
            self.run_btn.config(state="disabled")
            self.install_btn.config(state="normal")

    def is_installed(self, package):
        try:
            pkg_resources.get_distribution(package)
            return True
        except pkg_resources.DistributionNotFound:
            return False

    def add_status_row(self, name, status):
        row = tk.Frame(self.list_frame)
        row.pack(fill="x", pady=2)
        
        icon = "✔" if status else "✘"
        color = "green" if status else "red"
        
        tk.Label(row, text=icon, fg=color, font=("Arial", 12, "bold"), width=3).pack(side="left")
        tk.Label(row, text=name, font=("Arial", 10)).pack(side="left")
        status_text = "Telepítve" if status else "Hiányzik"
        tk.Label(row, text=status_text, fg="gray", font=("Arial", 9, "italic")).pack(side="right")

    def install_packages(self):
        """Meghívja a pip-et a hiányzó csomagokhoz."""
        for pkg in self.required_packages:
            if not self.is_installed(pkg):
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                except Exception as e:
                    messagebox.showerror("Hiba", f"Nem sikerült a(z) {pkg} telepítése: {e}")
        
        self.check_dependencies()
        messagebox.showinfo("Kész", "A telepítési folyamat befejeződött!")

    def start_app(self):
        messagebox.showinfo("Indítás", "A főprogram indul...")
        self.root.destroy()
        # Itt hívjuk meg a run.py-t vagy a fő logikát
        import run
        run.main()

if __name__ == "__main__":
    root = tk.Tk()
    app = SetupWizard(root)
    root.mainloop()
