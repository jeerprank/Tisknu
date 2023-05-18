import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedStyle
from win32 import win32api
from win32 import win32print
from PIL import Image, ImageTk

root = tk.Tk()
root.withdraw()
style = ThemedStyle(root)
icon_path = r"C:\Users\Jeer\Desktop\codin\Tiskačka\build\ico-8.png"
icon = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(True, icon)

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
