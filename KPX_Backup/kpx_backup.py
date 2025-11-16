import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
from datetime import datetime
import threading
import zipfile
import hashlib
import sys

# --- Configuration File ---
CONFIG_FILE = "config.json"
ICON_FILE = "backup-icon.png"

# --- Password Hashing ---
def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- Main Application Class ---
class KPXBackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KPX Backup - Keep Projects Xtra-safe")
        self.root.geometry("700x580")

        # --- NEW: Create the Menu Bar ---
        self.create_menu()

        # App State
        self.is_admin = False
        self.config = self.load_config()

        # --- FIX: Create Tkinter variables to link with the GUI ---
        self.source_path_var = tk.StringVar(value=self.config.get("source_path", ""))
        self.destination_path_var = tk.StringVar(value=self.config.get("destination_path", ""))
        self.schedule_day_var = tk.IntVar(value=self.config.get("schedule_day", 1))

        # Set icon if the file exists
        try:
            if hasattr(sys, '_MEIPASS'):
                icon_path = os.path.join(sys._MEIPASS, ICON_FILE)
            else:
                icon_path = ICON_FILE
            self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except Exception:
            # Silently ignore if the icon can't be loaded
            pass

        # --- Create GUI Elements ---
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        # --- Top Bar for Login ---
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        self.admin_button = ttk.Button(top_frame, text="Admin Login", command=self.show_login_window)
        self.admin_button.pack(side="left")

        self.status_indicator = ttk.Label(top_frame, text="🔒 User Mode", font=("Helvetica", 10))
        self.status_indicator.pack(side="right")

        # Title Label
        title_label = ttk.Label(main_frame, text="KPX Backup", font=("Helvetica", 24))
        title_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # --- Admin Settings Frame (Initially Disabled) ---
        self.admin_frame = ttk.LabelFrame(main_frame, text="Admin Settings", padding="10")
        self.admin_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)

        # Source Folder Selection
        ttk.Label(self.admin_frame, text="Source Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.source_entry = ttk.Entry(self.admin_frame, textvariable=self.source_path_var, width=50)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)
        self.source_browse_button = ttk.Button(self.admin_frame, text="Browse...", command=self.select_source)
        self.source_browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Destination Folder Selection
        ttk.Label(self.admin_frame, text="Destination Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.dest_entry = ttk.Entry(self.admin_frame, textvariable=self.destination_path_var, width=50)
        self.dest_entry.grid(row=1, column=1, padx=5, pady=5)
        self.dest_browse_button = ttk.Button(self.admin_frame, text="Browse...", command=self.select_destination)
        self.dest_browse_button.grid(row=1, column=2, padx=5, pady=5)

        # --- Automatic Backup Schedule ---
        ttk.Label(self.admin_frame, text="Auto-Backup Day (of month):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.schedule_spinbox = ttk.Spinbox(self.admin_frame, from_=1, to=31, textvariable=self.schedule_day_var, width=5)
        self.schedule_spinbox.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(self.admin_frame, text="Save Settings", command=self.save_admin_settings).grid(row=3, column=0, columnspan=3, pady=10)

        # --- User Controls ---
        user_frame = ttk.Frame(main_frame)
        user_frame.grid(row=3, column=0, columnspan=3, pady=20)

        self.backup_button = ttk.Button(user_frame, text="BACKUP", command=self.start_backup_thread)
        self.backup_button.pack()

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(main_frame, orient="horizontal", length=640, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        # Status Label
        self.status_label = ttk.Label(main_frame, text="Ready to backup.", wraplength=640)
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

        # --- FINAL STATE INITIALIZATION ---
        self._toggle_admin_frame()
        
        # --- Start the scheduler check ---
        self.schedule_check()

    def create_menu(self):
        """Creates the menu bar at the top of the application."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About KPX Backup", command=self.show_about_window)

    def show_about_window(self):
        """Displays the About/Credits window."""
        about_window = tk.Toplevel(self.root)
        about_window.title("About KPX Backup")
        about_window.geometry("400x250")
        about_window.resizable(False, False)
        about_window.transient(self.root)
        about_window.grab_set()

        # Center the window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (about_window.winfo_screenheight() // 2) - (250 // 2)
        about_window.geometry(f"400x250+{x}+{y}")

        # --- NEW: Use a main frame and a separate button frame for better layout ---
        main_content_frame = ttk.Frame(about_window, padding="20")
        main_content_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(main_content_frame, text="KPX Backup", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=(0, 5))

        subtitle_label = ttk.Label(main_content_frame, text="Keep Projects Xtra-safe", font=("Helvetica", 12))
        subtitle_label.pack(pady=(0, 20))

        credits_label = ttk.Label(main_content_frame, text="Created by: Klevis", font=("Helvetica", 12))
        credits_label.pack(pady=10)

        version_label = ttk.Label(main_content_frame, text="Version 1.0", font=("Helvetica", 10, "italic"))
        version_label.pack(pady=5)

        # --- NEW: A dedicated frame for the button ---
        button_frame = ttk.Frame(about_window)
        button_frame.pack(fill="x", padx=20, pady=(0, 15)) # Add padding at the bottom

        # --- IMPROVED: A wider, more prominent OK button ---
        ok_button = ttk.Button(button_frame, text="OK", command=about_window.destroy, width=15)
        ok_button.pack()

    def load_config(self):
        """Loads config and sets a default admin password if none exists."""
        default_config = {
            "source_path": "",
            "destination_path": "",
            "admin_password_hash": hash_password("admin"),
            "schedule_day": 1
        }
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

    def save_admin_settings(self):
        """Saves the paths and schedule set by the admin."""
        self.config["source_path"] = self.source_path_var.get()
        self.config["destination_path"] = self.destination_path_var.get()
        self.config["schedule_day"] = self.schedule_day_var.get()
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
        
        messagebox.showinfo("Success", "Admin settings have been saved.")
        self.status_label.config(text="✅ Settings saved.")

    def show_login_window(self):
        """Displays the login popup window."""
        login_window = tk.Toplevel(self.root)
        login_window.title("Admin Login")
        login_window.geometry("300x150")
        login_window.transient(self.root)
        login_window.grab_set()

        ttk.Label(login_window, text="Enter Admin Password:").pack(pady=10)
        password_entry = ttk.Entry(login_window, show="*", width=30)
        password_entry.pack(pady=5)
        password_entry.focus_set()

        def attempt_login():
            password = password_entry.get()
            if hash_password(password) == self.config.get("admin_password_hash"):
                self.is_admin = True
                self.status_indicator.config(text="🔓 Admin Mode")
                self.admin_button.config(text="Logout", command=self.logout)
                self._toggle_admin_frame()
                login_window.destroy()
            else:
                messagebox.showerror("Login Failed", "Incorrect password.", parent=login_window)

        ttk.Button(login_window, text="Login", command=attempt_login).pack(pady=10)
        login_window.bind('<Return>', lambda event: attempt_login())

    def logout(self):
        """Logs out the admin and disables admin controls."""
        self.is_admin = False
        self.status_indicator.config(text="🔒 User Mode")
        self.admin_button.config(text="Admin Login", command=self.show_login_window)
        self._toggle_admin_frame()

    def _toggle_admin_frame(self):
        """Enables or disables all widgets in the admin frame."""
        state = 'normal' if self.is_admin else 'disabled'
        for child in self.admin_frame.winfo_children():
            if isinstance(child, (ttk.Entry, ttk.Button, ttk.Spinbox)):
                child.config(state=state)

    def select_source(self):
        folder_selected = filedialog.askdirectory(title="Select Folder to Backup")
        if folder_selected:
            self.source_path_var.set(folder_selected)

    def select_destination(self):
        folder_selected = filedialog.askdirectory(title="Select Backup Destination")
        if folder_selected:
            self.destination_path_var.set(folder_selected)

    def start_backup_thread(self):
        source = self.source_path_var.get()
        destination = self.destination_path_var.get()

        if not source or not destination:
            messagebox.showerror("Error", "Backup paths are not set. Please contact an administrator.")
            return
        if not os.path.isdir(source):
            messagebox.showerror("Error", f"The source folder does not exist:\n{source}")
            return
        if not os.path.isdir(destination):
            messagebox.showerror("Error", f"The destination folder does not exist:\n{destination}")
            return

        self.backup_button.config(state="disabled")
        self.progress['value'] = 0
        self.status_label.config(text="Starting backup... Please wait.")
        self.root.update_idletasks()

        backup_thread = threading.Thread(target=self._backup_worker, args=(source, destination))
        backup_thread.start()

    def _backup_worker(self, source, destination):
        """This worker now ONLY creates zip files."""
        try:
            source_folder_name = os.path.basename(source)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            backup_file_name = f"{source_folder_name}_backup_{timestamp}.zip"
            full_destination_path = os.path.join(destination, backup_file_name)

            self.status_label.config(text="Counting files... This may take a moment.")
            total_files = sum(len(files) for _, _, files in os.walk(source))
            if total_files == 0:
                self.status_label.config(text="Source folder is empty. Nothing to backup.")
                self.backup_button.config(state="enabled")
                return

            self.progress['maximum'] = total_files
            files_copied = 0

            with zipfile.ZipFile(full_destination_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                for root, dirs, files in os.walk(source):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source)
                        backup_zip.write(file_path, arcname)
                        files_copied += 1
                        self.progress['value'] = files_copied

            self.status_label.config(text=f"✅ Backup successful!\nCreated at: {full_destination_path}")
            messagebox.showinfo("Success", "Backup completed successfully!")

        except Exception as e:
            self.status_label.config(text="❌ Backup failed.")
            messagebox.showerror("Backup Failed", f"An error occurred: {e}")
        finally:
            self.backup_button.config(state="enabled")

    def schedule_check(self):
        """Checks the date once an hour and triggers a backup if it's the scheduled day."""
        now = datetime.now()
        schedule_day = self.config.get("schedule_day", 1)
        
        if now.day == schedule_day and now.hour == 9 and now.minute < 5:
            self.status_label.config(text="🚀 Scheduled backup triggered!")
            self.start_backup_thread()

        self.root.after(3600000, self.schedule_check)


# --- Run the Application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = KPXBackupApp(root)
    root.mainloop()