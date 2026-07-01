# Fimi Notepad by Banton (Open Source)

Thank you for checking out this custom notepad utility. 

This application is designed to be **100% private, local, and safe**. It has zero telemetry, no advertising trackers, and requires no background app permissions or network connectivity. It strictly captures keyboard inputs to edit and save text locally on your computer.

### Features
* **Tabbed Interface:** Work on multiple files at once.
* **Smart Safety:** Warns you if you try to close unsaved tabs.
* **Standard Editing:** Cut, Copy, Paste, Undo, Redo, and Find & Replace.
* **100% Local:** No network, No cloud syncing, no data harvesting. 

---

## ⚠️ Why Might Antivirus Programs Flag This? (False Positives)

When running the compiled `fimi_notepad.exe` file, Windows SmartScreen or an antivirus engine may flag it as an "unsigned" or "unknown" executable. 

This is a common issue with Python scripts bundled using 'PyInstaller' because indie software lacks an expensive, enterprise digital signature from Microsoft. 

To ensure complete transparency, the exact Python source code used to build this program is provided right next to it (`fimi_notepad.py`). **You do not have to trust the executable—you can audit the code yourself.**

---

## 🔍 3 Independent Ways to Verify This Code is 100% Safe

If you do not want to rely on the creator's word, you can independently verify the safety of `fimi_notepad.py` using these three completely separate and unbiased methods:

### WAY 1: Line-by-Line Human Audit (No Programming Experience Needed)
Open `fimi_notepad.py` using a standard text editor. Look closely at the code. You will see that:
* It only uses `tkinter` (Python's built-in tool for desktop windows).
* It only uses `filedialog` and `messagebox` (for native window prompts).
* It does **NOT** import network modules like `socket`, `urllib`, or `requests`. Without these, the code is structurally isolated and physically cannot connect to the internet, open ports, or send data.

### WAY 2: Use an External AI Checker
You can use an AI platform to act as an independent, unbiased auditor. 
1. Go to ChatGPT (chatgpt.com) or Claude (claude.ai).
2. Copy and paste the contents of `fimi_notepad.py` into the prompt box.
3. Ask it exactly this: *"Analyze this Python code. Does it contain malicious functions, hidden trackers, keyloggers, or any commands attempting network connectivity?"*
4. Read the unbiased, architectural breakdown it provides.

### WAY 3: Compile It Yourself From Scratch (Zero-Trust Method)
If you want to use the program but do not trust the provided `fimi_notepad.exe`, you can delete it entirely and build your own copy directly from the raw `fimi_notepad.py` script. 
1. Install official Python from python.org.
2. Open your terminal/command prompt and type: `pip install pyinstaller`
3. Navigate to this folder and type: `pyinstaller --noconsole --onefile fimi_notepad.py`
4. Your computer will build a fresh, identical executable inside a newly created 'dist' folder. You now know with 100% certainty exactly what is inside your running file.

---

## 🔒 Official File Verification (Checksum)
To mathematically verify that your downloaded file is authentic and unaltered, compare its SHA-256 hash to the master hash below:

**Master SHA-256 Hash:** `22bf7b1222f788dd57537d7f9debcd56c2b66cac0161a74dc9343e1f695fac19`

*To check your file on Windows, open a command prompt in your download folder and run: `certutil -hashfile fimi_notepad.py SHA256`*

---
**Created by Banton.** Website: [banton.org](https://banton.org)