import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import fitz  # PyMuPDF
import requests

# --- API Config ---
DEEPSEEK_API_KEY = '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'
MODEL_ID = "deepseek/deepseek-prover-v2:free"
DEEPSEEK_URL = 'https://openrouter.ai/api/v1/chat/completions'

# --- Functional Logic ---
def extract_pdf_text(pdf_path, max_pages=3):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(max_pages, len(doc))):
        text += doc[page_num].get_text()
    doc.close()
    return text

def summarize_text(text):
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Summarize this academic research content in bullet points:\n\n{text}"

    data = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are a helpful academic assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(DEEPSEEK_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# --- GUI Setup ---
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_path.set(file_path)

def summarize_pdf():
    path = pdf_path.get()
    if not path:
        messagebox.showwarning("Warning", "Please select a PDF file.")
        return
    try:
        text = extract_pdf_text(path)
        summary = summarize_text(text)
        summary_text.delete(1.0, tk.END)
        summary_text.insert(tk.END, summary)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# --- Root Window ---
root = tk.Tk()
root.title("Research Paper Summarizer")
root.geometry("900x600")
root.configure(bg="#eaebfe")
root.resizable(False, False)

pdf_path = tk.StringVar()

# --- Style Setup ---
style = ttk.Style()
style.theme_use("clam")

style.configure("Rounded.TButton",
                background="#2c2776",
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                borderwidth=0,
                padding=8,
                relief="flat")

style.map("Rounded.TButton",
          background=[("active", "#3a378a")])

style.configure("Vertical.TScrollbar",
                gripcount=0,
                background="#c2c2f0", darkcolor="#c2c2f0", lightcolor="#c2c2f0",
                troughcolor="#eaebfe", bordercolor="#eaebfe", arrowcolor="#2c2776",
                relief="flat")

# --- Main Frame ---
main_frame = tk.Frame(root, bg="#eaebfe")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Label
label = tk.Label(main_frame, text="Select PDF:", font=("Segoe UI", 10), bg="#eaebfe")
label.grid(row=0, column=0, sticky="w", pady=5)

# Entry
entry_frame = tk.Frame(main_frame, bg="white", highlightbackground="#ccc", highlightthickness=1)
entry_frame.grid(row=0, column=1, sticky="ew", padx=(5, 5), pady=5)
entry_frame.grid_columnconfigure(0, weight=1)

entry = tk.Entry(entry_frame, textvariable=pdf_path,
                 font=("Segoe UI", 10), relief="flat",
                 bg="white", bd=0)
entry.grid(row=0, column=0, sticky="ew", ipadx=10, ipady=6)

# Browse Button
browse_button = ttk.Button(
    main_frame, text="Browse", command=browse_file,
    style="Rounded.TButton"
)
browse_button.grid(row=0, column=2, padx=(5, 0), pady=5)

# Summarize Button
summarize_button = ttk.Button(
    main_frame, text="Summarize", command=summarize_pdf,
    style="Rounded.TButton"
)
summarize_button.grid(row=1, column=0, columnspan=3, pady=15)

# Output Label
output_label = tk.Label(main_frame, text="Summary Output:", font=("Segoe UI", 10, "bold"), bg="#eaebfe")
output_label.grid(row=2, column=0, columnspan=3, sticky="w", pady=(10, 5))

# Text Frame
text_frame = tk.Frame(main_frame, bg="#eaebfe", highlightthickness=1, highlightbackground="#ccc")
text_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

# Scrollbar
scrollbar = ttk.Scrollbar(text_frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

# Text Box
summary_text = tk.Text(
    text_frame, wrap="word", font=("Segoe UI", 10), bg="white",
    relief="flat", padx=10, pady=10, yscrollcommand=scrollbar.set, bd=0
)
summary_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=summary_text.yview)

# Grid weight config
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(3, weight=1)

# --- Run ---
root.mainloop()
