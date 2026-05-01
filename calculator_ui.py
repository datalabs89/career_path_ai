import tkinter as tk
from tkinter import messagebox
from calculator import evaluate

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("360x520")
        self.root.configure(bg="#1E1E24")
        self.root.resizable(False, False)

        # Style configurations
        self.font_large = ("Helvetica", 32, "bold")
        self.font_medium = ("Helvetica", 18)
        self.color_bg = "#1E1E24"
        self.color_display_bg = "#292930"
        self.color_text = "#FFFFFF"
        self.color_btn = "#33333D"
        self.color_btn_hover = "#454552"
        self.color_operator = "#FF9500"
        self.color_operator_hover = "#FFB03B"
        self.color_clear = "#D9534F"
        self.color_clear_hover = "#E26A66"

        self.expression = ""

        self.setup_ui()

    def setup_ui(self):
        # Display Area
        display_frame = tk.Frame(self.root, bg=self.color_display_bg, bd=0)
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_label = tk.Label(
            display_frame, 
            textvariable=self.display_var, 
            font=self.font_large, 
            bg=self.color_display_bg, 
            fg=self.color_text, 
            anchor="e", 
            padx=20, 
            pady=20
        )
        display_label.pack(expand=True, fill="both")

        # Buttons Area
        buttons_frame = tk.Frame(self.root, bg=self.color_bg)
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Grid configuration for buttons
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)

        buttons = [
            ("C", 0, 0, 1, self.color_clear, self.color_clear_hover), 
            ("(", 0, 1, 1, self.color_btn, self.color_btn_hover), 
            (")", 0, 2, 1, self.color_btn, self.color_btn_hover), 
            ("/", 0, 3, 1, self.color_operator, self.color_operator_hover),
            
            ("7", 1, 0, 1, self.color_btn, self.color_btn_hover), 
            ("8", 1, 1, 1, self.color_btn, self.color_btn_hover), 
            ("9", 1, 2, 1, self.color_btn, self.color_btn_hover), 
            ("*", 1, 3, 1, self.color_operator, self.color_operator_hover),
            
            ("4", 2, 0, 1, self.color_btn, self.color_btn_hover), 
            ("5", 2, 1, 1, self.color_btn, self.color_btn_hover), 
            ("6", 2, 2, 1, self.color_btn, self.color_btn_hover), 
            ("-", 2, 3, 1, self.color_operator, self.color_operator_hover),
            
            ("1", 3, 0, 1, self.color_btn, self.color_btn_hover), 
            ("2", 3, 1, 1, self.color_btn, self.color_btn_hover), 
            ("3", 3, 2, 1, self.color_btn, self.color_btn_hover), 
            ("+", 3, 3, 1, self.color_operator, self.color_operator_hover),
            
            ("0", 4, 0, 2, self.color_btn, self.color_btn_hover), 
            (".", 4, 2, 1, self.color_btn, self.color_btn_hover), 
            ("=", 4, 3, 1, self.color_operator, self.color_operator_hover)
        ]

        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            colspan = btn[3]
            bg_color = btn[4]
            hover_color = btn[5]

            self.create_button(buttons_frame, text, row, col, colspan, bg_color, hover_color)

    def create_button(self, parent, text, row, col, colspan, bg_color, hover_color):
        btn = tk.Button(
            parent, 
            text=text, 
            font=self.font_medium, 
            bg=bg_color, 
            fg=self.color_text, 
            bd=0, 
            activebackground=hover_color, 
            activeforeground=self.color_text,
            relief="flat",
            command=lambda t=text: self.on_button_click(t)
        )
        
        # Hover effects
        btn.bind("<Enter>", lambda e, b=btn, c=hover_color: b.config(bg=c))
        btn.bind("<Leave>", lambda e, b=btn, c=bg_color: b.config(bg=c))
        
        btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set("0")
        elif char == "=":
            try:
                if self.expression:
                    # Using evaluate from calculator.py
                    result = evaluate(self.expression)
                    # Formatting to remove trailing .0 if integer
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    
                    self.display_var.set(str(result))
                    self.expression = str(result)
            except Exception as e:
                self.display_var.set("Error")
                self.expression = ""
        else:
            if self.expression == "0" and char not in ".+-*/":
                self.expression = char
            else:
                self.expression += char
            
            self.display_var.set(self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    
    # Optional: Set app icon or configure styles further here
    
    root.mainloop()
