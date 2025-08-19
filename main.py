import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Treeview
import pandas as pd
import os
from ranker import rank_resumes

def run_ranking():
    jd_text = jd_textbox.get("1.0", tk.END).strip()
    folder_path = folder_var.get()

    if not jd_text:
        messagebox.showerror("Error", "Please enter a job description.")
        return
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Please select a valid folder containing resumes.")
        return

    df = rank_resumes(jd_text, folder_path)
    display_results(df)
    export_button.config(state="normal")
    global last_result_df
    last_result_df = df

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)

def display_results(df):
    for widget in result_frame.winfo_children():
        widget.destroy()

    if df.empty:
        tk.Label(result_frame, text="No resumes matched.").pack()
        return

    tree = Treeview(result_frame, columns=list(df.columns), show="headings")
    for col in df.columns:
        width = 150
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="w")
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))
    tree.pack(expand=True, fill='both')

def export_results():
    if last_result_df is not None:
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if save_path:
            last_result_df.to_csv(save_path, index=False)
            messagebox.showinfo("Export Successful", f"Results saved to {save_path}")

def create_gui():
    global jd_textbox, folder_var, result_frame, export_button, last_result_df
    last_result_df = None

    root = tk.Tk()
    root.title("Resume Ranking System")
    root.geometry("1000x600")

    tk.Label(root, text="Job Description:").pack(anchor="w", padx=10, pady=5)
    jd_textbox = scrolledtext.ScrolledText(root, height=6, wrap=tk.WORD)
    jd_textbox.pack(fill="x", padx=10, pady=5)

    folder_var = tk.StringVar()
    tk.Label(root, text="Select Resume Folder:").pack(anchor="w", padx=10, pady=5)
    folder_frame = tk.Frame(root)
    folder_frame.pack(fill="x", padx=10)
    tk.Entry(folder_frame, textvariable=folder_var, width=60).pack(side="left", fill="x", expand=True)
    tk.Button(folder_frame, text="Browse", command=browse_folder).pack(side="left", padx=5)

    tk.Button(root, text="Rank Resumes", command=run_ranking, bg="green", fg="white").pack(pady=10)

    export_button = tk.Button(root, text="Download Results", command=export_results, bg="blue", fg="white", state="disabled")
    export_button.pack(pady=5)

    result_frame = tk.Frame(root)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()