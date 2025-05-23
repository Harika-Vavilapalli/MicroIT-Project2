import tkinter as tk

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.configure(bg="black")
        self.geometry("300x450")
        self.expression = ""

        self.create_widgets()

    def create_widgets(self):
        self.display = tk.Entry(self, font=("Arial", 24), bg="black", fg="white", bd=0, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=25, sticky="nsew")

        self.result_display = tk.Label(self, text="", font=("Arial", 16), fg="gray", bg="black", anchor="e")
        self.result_display.grid(row=1, column=0, columnspan=4, sticky="nsew")

        buttons = [
            ("AC", 2, 0), ("%", 2, 1), ("⌫", 2, 2), ("÷", 2, 3),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("×", 3, 3),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("−", 4, 3),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("+", 5, 3),
            ("00", 6, 0), ("0", 6, 1), (".", 6, 2), ("=", 6, 3),
        ]

        for (text, row, col) in buttons:
            button = tk.Button(self, text=text, font=("Arial", 18), fg="white", bg="black",
                               activebackground="gray", bd=0, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew", padx=1, pady=1, ipadx=10, ipady=20)

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "AC":
            self.expression = ""
            self.display.delete(0, tk.END)
            self.result_display.config(text="")
        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
        elif char == "=":
            try:
                expression = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
                result = eval(expression)
                self.result_display.config(text=str(result))
            except Exception:
                self.result_display.config(text="Error")
        else:
            self.expression += char
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
