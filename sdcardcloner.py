import tkinter as tk
from tkinter import ttk, filedialog
import subprocess

class ProgressDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Progress")
        self.geometry("400x80")
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=20)

    def update_progress(self, current, total):
        percent = int((current / total) * 100)
        self.progress_bar["value"] = percent
        self.update_idletasks()

class SDCardClonerGUI:
    def __init__(self, master):
        self.master = master
        master.title("SD Card Cloner")

        self.source_label = tk.Label(master, text="Source SD Card:")
        self.source_label.grid(row=0, column=0, padx=10, pady=10)

        self.source_entry = tk.Entry(master, width=50)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10)

        self.source_browse_button = tk.Button(master, text="Browse", command=self.browse_source)
        self.source_browse_button.grid(row=0, column=2, padx=10, pady=10)

        self.target_label = tk.Label(master, text="Target SD Card:")
        self.target_label.grid(row=1, column=0, padx=10, pady=10)

        self.target_entry = tk.Entry(master, width=50)
        self.target_entry.grid(row=1, column=1, padx=10, pady=10)

        self.target_browse_button = tk.Button(master, text="Browse", command=self.browse_target)
        self.target_browse_button.grid(row=1, column=2, padx=10, pady=10)

        self.bs_label = tk.Label(master, text="Block Size (e.g., 4M):")
        self.bs_label.grid(row=2, column=0, padx=10, pady=10)

        self.bs_entry = tk.Entry(master, width=10)
        self.bs_entry.insert(0, "4M")  # Default block size is set to 4M
        self.bs_entry.grid(row=2, column=1, padx=10, pady=10)

        self.clone_button = tk.Button(master, text="Clone SD Card", command=self.clone_sd_card)
        self.clone_button.grid(row=3, column=0, pady=20)

        self.flash_button = tk.Button(master, text="Flash SD Card", command=self.flash_sd_card)
        self.flash_button.grid(row=3, column=1, pady=20)

    def browse_source(self):
        source_path = filedialog.askopenfilename(title="Select Source SD Card")
        if source_path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, source_path)

    def browse_target(self):
        target_path = filedialog.askopenfilename(title="Select Target SD Card")
        if target_path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, target_path)

    def clone_sd_card(self):
        source_path = self.source_entry.get()
        target_path = self.target_entry.get()
        bs = self.bs_entry.get()

        if source_path and target_path:
            progress_dialog = ProgressDialog(self.master)
            dd_command = f"sudo dd if={source_path} of={target_path} bs={bs} status=progress"
            self.run_dd_command(dd_command, progress_dialog)
            progress_dialog.destroy()  # Close the progress bar window
            tk.messagebox.showinfo("Success", "SD Card Cloning Completed!")
        else:
            tk.messagebox.showerror("Error", "Please select both source and target SD cards.")

    def flash_sd_card(self):
        source_path = self.source_entry.get()
        target_path = self.target_entry.get()
        bs = self.bs_entry.get()

        if source_path and target_path:
            progress_dialog = ProgressDialog(self.master)
            dd_command = f"sudo dd if={source_path} of={target_path} bs={bs} status=progress"
            self.run_dd_command(dd_command, progress_dialog)
            progress_dialog.destroy()  # Close the progress bar window
            tk.messagebox.showinfo("Success", "SD Card Flashing Completed!")
        else:
            tk.messagebox.showerror("Error", "Please select both source and target SD cards.")

    def run_dd_command(self, dd_command, progress_dialog):
        process = subprocess.Popen(dd_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for line in process.stdout:
            if "bytes" in line:
                parts = line.split()
                if len(parts) == 7:
                    current_bytes = int(parts[0])
                    total_bytes = int(parts[4])
                    progress_dialog.update_progress(current_bytes, total_bytes)

        process.wait()

if __name__ == "__main__":
    root = tk.Tk()
    app = SDCardClonerGUI(root)
    root.mainloop()
