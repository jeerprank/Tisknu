# Tisknu

This code is a Python script that utilizes the `tkinter` library to create a graphical user interface (GUI) for printing files. The script allows the user to select a file and choose a printer from a dropdown menu to initiate the printing process. It also includes a button that can be used to change the GUI theme.

## Prerequisites
Before running this code, make sure you have the following prerequisites installed:
- Python: Make sure you have Python installed on your system.
- Required Libraries: Install the required libraries by running the following command:
  ```
  pip install tkinter ttkthemes pywin32 pillow
  ```

## Code Explanation
Let's go through the code section by section to understand its functionality.

```python
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedStyle
from win32 import win32api
from win32 import win32print
from PIL import Image, ImageTk
```
The code begins by importing the necessary libraries. `tkinter` is imported as `tk` for creating the GUI components, while `ttk` is imported separately for the themed button and combobox. `filedialog` is imported from `tkinter` to provide a file selection dialog. `ThemedStyle` is imported from `ttkthemes` to enable theme customization. `win32api` and `win32print` are imported from `win32` for printer-related functionality. `Image` and `ImageTk` are imported from `PIL` (Pillow) to handle images in the GUI.

```python
root = tk.Tk()
root.withdraw()
```
Here, a new `Tk` object is created, but its main window is immediately withdrawn (hidden) using the `withdraw()` method. This allows the script to create additional windows later without showing the main window.

```python
style = ThemedStyle(root)
icon_path = r"C:\Users\Jeer\Desktop\codin\Tiskačka\build\ico-8.png"
icon = ImageTk.PhotoImage(Image.open(icon_path))
root.iconphoto(True, icon)
```
A `ThemedStyle` object is created, associated with the root window. This enables theme customization for the GUI components. An icon image is loaded from the specified path using `Image.open()` and converted into an `ImageTk.PhotoImage` object. The icon is then set as the application icon using `root.iconphoto()`.

```python
style.theme_use("equilux")
style.configure("TCombobox", fieldbackground="white", background="white")
style.configure("TButton", foreground="white")
style.configure(".", font=("Gantari SemiBold", 10))
```
The GUI theme is set to "equilux" using `style.theme_use()`. This can be customized to any other theme supported by `ttkthemes`. Next, various styles are configured using `style.configure()`. The combobox (`TCombobox`) and button (`TButton`) are customized to have a white background and white foreground (text color). The font for all components is set to "Gantari SemiBold" with a size of 10.

```python
def change_theme():
    if style.theme_use() == "equilux":
        style.theme_use("default")
    else:
        style.theme_use("equilux")
```
This function is triggered when the "Change theme!" button is clicked. It checks the currently used theme and toggles between "equilux" and "default" themes using `style.theme_use()`.

```python
def print_files(file_path):
    printers = win32print.EnumPrinters(2)
    printer_names = [

printer[2] for printer in printers]

    pt = tk.Toplevel()
    pt.geometry("320x180")
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
```
This function creates a new top-level window (`Toplevel`) for selecting a printer and initiating the printing process. It takes a `file_path` argument but doesn't use it directly (will be explained later). First, it retrieves the list of available printers using `win32print.EnumPrinters(2)` and extracts the printer names from the obtained data. Then, a new top-level window is created with a fixed size of 320x180 and titled "Tisknu" (Czech for "Printing").

Inside the window, a label (`LABEL`) is created to prompt the user to select a printer. A combobox (`PRCOMBO`) is created using `ttk.Combobox`, which allows the user to choose a printer from the available options. The combobox is configured with a width of 35, using the previously configured combobox style and font.

A custom progress bar style (`Custom.Horizontal.TProgressbar`) is defined using `style.configure()`. The progress bar (`PROGRESS_BAR`) is then created with a length of 200, an indeterminate mode, and the custom style. It is also configured to have a white background and white progress trough.

A button (`BUTTON`) is created with the text "Tisknout" (Czech for "Print") and a command that calls the `print_selected_file()` function, passing the `file_path`, selected printer name, and progress bar as arguments. The button is styled using the previously configured button style.

```python
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
```
This function is responsible for printing the selected file. It creates a new `Tk` object and immediately hides its main window. Then, it opens a file selection dialog using `filedialog.askopenfilename()` to allow the user to choose a file to print. The selected file path is stored in the `file_path` variable.

The selected file is opened and read line by line. The total number of lines is determined using `len(lines)`. The progress bar's maximum value is set accordingly using `progress_bar.configure()`. 

Inside the loop,

 each line is stripped of leading/trailing whitespace and split into `file_name` and `directory` using the colon (':') delimiter. `win32api.ShellExecute()` is called to initiate the printing of the specified `directory` with the selected `printer_name`.

After each iteration, the progress bar is updated using `progress_bar.step()` and `progress_bar.update()`. Finally, when the loop is complete, the progress bar is stopped using `progress_bar.stop()`.

```python
print_files('file.txt')

button = ttk.Button(root, text="Change theme!", command=change_theme)
button.pack()

root.mainloop()
```
The `print_files()` function is called with the argument `'file.txt'`, which represents the path of the file to be printed.

A button (`button`) is created using `ttk.Button` and added to the root window. It has the text "Change theme!" and triggers the `change_theme()` function when clicked.

Finally, the main event loop is started using `root.mainloop()`, which waits for user interactions and keeps the GUI running until the user closes the windows or exits the program.

## Conclusion
This code demonstrates how to create a GUI using `tkinter` and perform file printing operations using `win32print`. It provides a user-friendly interface for selecting a printer and initiating the printing process. The code also includes the option to change the GUI theme and supports theme customization.

Remember to adjust the file paths and customize the font styles and themes according to your needs.