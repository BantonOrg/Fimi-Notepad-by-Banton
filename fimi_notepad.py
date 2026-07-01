import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FimiNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Fimi Notepad by Banton")
        self.root.geometry("800x600")
        
        # Try to load the watermark for the window icon and about tab
        self.logo_img = None
        try:
            self.logo_img = tk.PhotoImage(file="bi1.png")
            self.root.iconphoto(False, self.logo_img)
        except Exception:
            pass # Fails silently if bi1.png is missing

        # Setup Notebook (Tabs manager)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        
        # Dictionary to track our open tabs {widget_name: data}
        self.tabs = {}
        
        self.create_menus()
        self.add_tab() # Open an initial blank tab
        
        # Bind the window close button to our safety check
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menus(self):
        menu_bar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New Tab", command=self.add_tab)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Close Tab", command=self.close_current_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: self.current_text_area().event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", command=lambda: self.current_text_area().event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.current_text_area().event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.current_text_area().event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.current_text_area().event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.find_replace_dialog)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About / Verification", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def current_text_area(self):
        # Helper to get the text area of the currently visible tab
        current_tab = self.notebook.select()
        if current_tab:
            return self.tabs[current_tab]["text_area"]
        return None

    def add_tab(self, filename="Untitled", content="", filepath=None):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=filename)
        
        text_area = tk.Text(frame, undo=True, wrap="word", font=("Arial", 11))
        scrollbar = tk.Scrollbar(frame, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        text_area.pack(side="left", fill="both", expand=True)
        
        if content:
            text_area.insert("1.0", content)
            
        # Track modifications to warn about unsaved changes
        text_area.edit_modified(False)
        text_area.bind("<<Modified>>", lambda e, f=str(frame): self.mark_unsaved(f))
        
        self.tabs[str(frame)] = {
            "text_area": text_area,
            "filepath": filepath,
            "saved": True
        }
        
        self.notebook.select(frame)
        return text_area

    def mark_unsaved(self, frame_id):
        if frame_id in self.tabs:
            text_area = self.tabs[frame_id]["text_area"]
            if text_area.edit_modified():
                self.tabs[frame_id]["saved"] = False
                current_text = self.notebook.tab(frame_id, "text")
                if not current_text.endswith("*"):
                    self.notebook.tab(frame_id, text=current_text + "*")
            text_area.edit_modified(False)

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            filename = filepath.split("/")[-1]
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            self.add_tab(filename=filename, content=content, filepath=filepath)

    def save_file(self):
        current_tab = self.notebook.select()
        if not current_tab: return
        
        tab_data = self.tabs[current_tab]
        filepath = tab_data["filepath"]
        
        if not filepath:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if not filepath: return
            tab_data["filepath"] = filepath
            filename = filepath.split("/")[-1]
            self.notebook.tab(current_tab, text=filename)
            
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(tab_data["text_area"].get(1.0, tk.END).rstrip())
            
        tab_data["saved"] = True
        current_text = self.notebook.tab(current_tab, "text").replace("*", "")
        self.notebook.tab(current_tab, text=current_text)

    def close_current_tab(self):
        current_tab = self.notebook.select()
        if not current_tab: return
        
        if not self.tabs[current_tab]["saved"]:
            filename = self.notebook.tab(current_tab, "text").replace("*", "")
            confirm = messagebox.askyesnocancel("Unsaved Changes", f"Save changes to {filename} before closing?")
            if confirm: # Yes
                self.save_file()
            elif confirm is None: # Cancel
                return
                
        self.notebook.forget(current_tab)
        del self.tabs[current_tab]

    def find_replace_dialog(self):
        text_area = self.current_text_area()
        if not text_area: return

        dialog = tk.Toplevel(self.root)
        dialog.title("Find & Replace")
        dialog.geometry("300x150")
        dialog.attributes('-topmost', True)

        tk.Label(dialog, text="Find:").grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(dialog)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(dialog)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        def find_text():
            text_area.tag_remove("search", "1.0", tk.END)
            target = find_entry.get()
            if target:
                idx = "1.0"
                while True:
                    idx = text_area.search(target, idx, nocase=True, stopindex=tk.END)
                    if not idx: break
                    lastidx = f"{idx}+{len(target)}c"
                    text_area.tag_add("search", idx, lastidx)
                    idx = lastidx
                text_area.tag_config("search", background="yellow")

        def replace_text():
            target = find_entry.get()
            replacement = replace_entry.get()
            if target:
                content = text_area.get("1.0", tk.END)
                new_content = content.replace(target, replacement)
                text_area.delete("1.0", tk.END)
                text_area.insert("1.0", new_content)

        tk.Button(dialog, text="Find All", command=find_text).grid(row=2, column=0, pady=10)
        tk.Button(dialog, text="Replace All", command=replace_text).grid(row=2, column=1, pady=10)

    def show_about(self):
        about_text = """
=========================================================
                 FIMI NOTEPAD BY BANTON
=========================================================

WHAT IS THIS?
This is a 100% private, local desktop notepad built to 
keep your thoughts safe from telemetry and trackers.

HOW TO VERIFY:
1. Read the provided 'fimi_notepad.py' code yourself.
2. Paste the code into any AI for an unbiased audit.
3. Compile it yourself using PyInstaller.

=========================================================
THANK YOU FOR USING FIMI NOTEPAD!
Created by Banton. 

Website: https://banton.org
Code: https://github.com/BantonOrg/Fimi-Notepad-by-Banton
=========================================================
"""
        # Open a new tab for the about section
        text_area = self.add_tab(filename="About Fimi", content=about_text)
        
        # Insert watermark image if it loaded successfully
        if self.logo_img:
            text_area.insert("1.0", "\n")
            text_area.image_create("1.0", image=self.logo_img)
            text_area.insert("1.0", "\n")
            
        # Lock the text area so it cannot be edited
        text_area.config(state="disabled")
        # Mark as saved so it doesn't trigger warnings on close
        current_tab = self.notebook.select()
        self.tabs[current_tab]["saved"] = True

    def on_closing(self):
        unsaved_count = sum(1 for tab in self.tabs.values() if not tab["saved"])
        if unsaved_count > 0:
            if not messagebox.askyesno("Unsaved Files", f"You have {unsaved_count} unsaved file(s). Are you sure you want to exit and lose changes?"):
                return
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FimiNotepad(root)
    root.mainloop()