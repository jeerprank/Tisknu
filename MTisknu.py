import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedStyle
from tkinter import font
from win32 import win32api
from win32 import win32print
import os
import sys
import matplotlib.font_manager as fm

root = tk.Tk()
root.withdraw()
style = ThemedStyle(root)
exe_dir = os.path.dirname(sys.executable)
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
fonts_dir = os.path.join(script_dir, "fonts")

custom_fonts = []
for font_file in os.listdir(fonts_dir):
    if font_file.endswith(".ttf"):
        font_path = os.path.join(fonts_dir, font_file)
        font_name = os.path.splitext(font_file)[0]
        installed_fonts = [f.name for f in fm.fontManager.ttflist]
        if font_name not in installed_fonts:
            try:
                fm.fontManager.addfont(font_path)
            except fm.FontManagerError:
                print(f"Failed to install font: {font_name}")
            else:
                print(f"Font installed: {font_name}")

        custom_font = font.Font(family=font_name, name=font_name)
        custom_fonts.append(custom_font)

style.theme_use("equilux")
style.configure("TCombobox", fieldbackground="white", background="white")
style.configure("TButton", foreground="white")
style.configure(".", font=("Gantari SemiBold", 13))

def change_theme():
    if style.theme_use() == "equilux":
        style.theme_use("default")
    else:
        style.theme_use("equilux")

def print_files(file_path):
    printers = win32print.EnumPrinters(2)
    printer_names = [printer[2] for printer in printers]

    pt = tk.Toplevel()
    pt.geometry("450x150")
    pt.title("Tisknu")

    font_style = ("Gantari SemiBold", 12)
    LABEL = tk.Label(pt, text="Vyber tiskárnu", fg="black", font=font_style)
    LABEL.pack()

    PRCOMBO = ttk.Combobox(pt, width=35, values=printer_names, style="TCombobox", font=font_style)
    PRCOMBO.pack()

    style.configure("Custom.Horizontal.TProgressbar", troughcolor="white", background="white")
    PROGRESS_BAR = ttk.Progressbar(pt, orient="horizontal", length=200, mode="indeterminate", style="Custom.Horizontal.TProgressbar")
    PROGRESS_BAR.pack(pady=10)

    BUTTON = ttk.Button(pt, text="Tisknout", command=lambda: print_selected_file(file_path, PRCOMBO.get(), PROGRESS_BAR), style="TButton")
    BUTTON.pack()

def print_selected_file(file_path, printer_name, progress_bar):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as f:
        lines = f.readlines()
        total_lines = len(lines)
        progress_bar.configure(maximum=total_lines)

        for index, line in enumerate(lines):
            file_name, directory = line.strip().split(':')
            win32api.ShellExecute(0, "print", directory, '/{}'.format(printer_name), ".", 0)
            progress_bar.step()
            progress_bar.update()

    progress_bar.stop()

print_files('file.txt')

button = ttk.Button(root, text="Change theme!", command=change_theme)
button.pack()

root.mainloop()
