import tkinter as tk
from tkinter import filedialog

class ShoppingListApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()



    def create_widgets(self):
        self.file_chooser = tk.Button(self.master, text='Pick file')
        self.file_chooser["command"] = self.chooser_callback
        self.file_chooser.grid(row=0, column=0, columnspan=2)

        self.factor_entry_label = tk.Label(self.master, text='Apply factor: ')
        self.factor_entry_label.grid(row=1, column=0)
        self.factor_entry = tk.Entry(self.master, text='Put factor')
        self.factor_entry.grid(row=1, column=1)

        self.generate_button = tk.Button(self.master, text="Generate")
        self.generate_button.grid(row=2, column=0, columnspan=2)

    def chooser_callback(self):
        filename = self.select_PDF()
        if filename:
            self.file_chooser["text"] = filename

    def select_PDF(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        return filename

root = tk.Tk()
app = ShoppingListApp(master=root)
app.mainloop()