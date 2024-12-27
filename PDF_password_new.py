import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
import threading
import time

# Global variable to control the pause state
is_paused = False

def brute_force_pdf_password(pdf_file_path, password_list_path):
    global is_paused
    # Open the PDF file
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Check if the PDF is encrypted
        if not pdf_reader.is_encrypted:
            log_message("The PDF file is not encrypted.")
            return

        # Attempt to read the password list with different encodings
        encodings = ['utf-8', 'utf-16', 'latin-1']  # Add more encodings if needed
        passwords = []
        for encoding in encodings:
            try:
                with open(password_list_path, 'r', encoding=encoding) as password_file:
                    passwords = password_file.readlines()
                break  # Exit the loop if successful
            except UnicodeDecodeError:
                log_message(f"Error reading the password list file with encoding: {encoding}")

        if not passwords:
            log_message("Failed to read the password list file with all attempted encodings.")
            return

        # Attempt to decrypt the PDF with each password
        for i, password in enumerate(passwords):
            password = password.strip()  # Remove any whitespace/newline characters

            # Check if the process is paused
            while is_paused:
                root.update_idletasks()
                time.sleep(0.1)

            log_message(f"Trying password {i + 1}/{len(passwords)}: {password}")

            try:
                if pdf_reader.decrypt(password):
                    log_message(f"Password found: {password}")
                    return
            except Exception as e:
                log_message(f"Error trying password '{password}': {e}")

            root.update_idletasks()

        log_message("Password not found in the provided list.")

def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_file_entry.delete(0, tk.END)
    pdf_file_entry.insert(0, file_path)

def select_password_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    password_file_entry.delete(0, tk.END)
    password_file_entry.insert(0, file_path)

def start_brute_force():
    global is_paused
    is_paused = False
    pdf_file_path = pdf_file_entry.get()
    password_list_path = password_file_entry.get()
    if pdf_file_path and password_list_path:
        log_message("Starting brute force...")
        # Run brute_force_pdf_password in a separate thread
        threading.Thread(target=brute_force_pdf_password, args=(pdf_file_path, password_list_path)).start()
    else:
        messagebox.showerror("Error", "Please select both PDF file and password list file.")

def pause_brute_force():
    global is_paused
    is_paused = not is_paused
    pause_button.config(text="Resume" if is_paused else "Pause")

def log_message(message):
    log_text.insert(tk.END, message + "\n")
    log_text.yview(tk.END)

# Create the main application window
root = tk.Tk()
root.title("PDF Password Brute Force Tool")

# Create and place widgets
tk.Label(root, text="PDF File:").grid(row=0, column=0, padx=10, pady=5)
pdf_file_entry = tk.Entry(root, width=50)
pdf_file_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_pdf_file).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Password List File:").grid(row=1, column=0, padx=10, pady=5)
password_file_entry = tk.Entry(root, width=50)
password_file_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_password_file).grid(row=1, column=2, padx=10, pady=5)

start_button = tk.Button(root, text="Start", command=start_brute_force)
start_button.grid(row=2, column=0, padx=10, pady=10)

pause_button = tk.Button(root, text="Pause", command=pause_brute_force)
pause_button.grid(row=2, column=1, padx=10, pady=10)

# Add a text area for logging
log_text = tk.Text(root, height=10, width=60)
log_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Run the application
root.mainloop()
