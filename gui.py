# Creator: Ian Zalewski on 5.7.2026
# For: Research with Proffesor Andrea Dernbecher
# Purpose: Use previous functions and programs in a easy to use GUI


import tkinter as tk
from tkinter import ttk


class imageSegmenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Processing for Pyrolosis Research")
        
        # Build the layout elements cleanly
        self.create_widgets()

    def create_widget():
        inputFrame = tk.Frame()

        combobox = ttk.Combobox(inputFrame, values=["Circle", "Rectangle"])
        combobox.set("One")
        #combobox.bind("<<ComboboxSelected>>", selection_changed)
        combobox.grid(row=1, column = 1, padx=5, pady=5, fill="x")





        label = tk.Label(text="Name", master=inputFrame)
        entry = tk.Entry(master=inputFrame)
        button = tk.Button(master= inputFrame)

        label.grid(row=0, column=0, padx=5, pady=5)
        entry.grid(row=0, column=1, padx=5, pady=5)
        button.grid(row=0, column=2, padx=5, pady=5)

        inputFrame.pack()




if __name__ == "__main__":
    app = imageSegmenterApp()
    app.mainloop()
