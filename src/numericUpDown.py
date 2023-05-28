import tkinter as tk

class NumericUpDown(tk.Frame):
    def __init__(self, master, min_value=1, max_value=10, initial_value=1, entry_width=5):
        super().__init__(master)

        self.min_value = min_value
        self.max_value = max_value

        self.var = tk.StringVar(value=str(initial_value))
        self.entry = tk.Entry(self, textvariable=self.var, width=entry_width)
        self.entry.pack(side=tk.LEFT)

        self.up_button = tk.Button(self, text="+", command=self.increment)
        self.up_button.pack(side=tk.LEFT)

        self.down_button = tk.Button(self, text="-", command=self.decrement)
        self.down_button.pack(side=tk.LEFT)

    def get(self):
        return int(self.var.get())

    def set(self, value):
        try:
            value = int(value)
            if value < self.min_value:
                raise ValueError("Value is too small")
            elif value > self.max_value:
                raise ValueError("Value is too large")
            self.var.set(str(value))
        except ValueError as e:
            # Display an error message if the input is invalid
            tk.messagebox.showerror("Error", str(e))

    def increment(self):
        value = self.get()
        if value < self.max_value:
            self.set(value + 1)

    def decrement(self):
        value = self.get()
        if value > self.min_value:
            self.set(value - 1)
    
    def update_value(self):
        value = self.get()
        if value < self.min_value:
            self.set(self.min_value)
        elif value > self.max_value:
            self.set(self.max_value)
            