#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 Cyberxjn GUI Calculator 
Modern looking calculator with dark theme for Kali Linux
Scientific functions + History + Variables
Author: Cyberxjn | 2026
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import re

class CyberxjnCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Cyberxjn Calculator")
        self.root.geometry("450x700")
        self.root.configure(bg='#1e1e1e')
        
        # Dark theme colors
        self.bg_color = '#1e1e1e'
        self.fg_color = '#ffffff'
        self.btn_bg = '#2d2d2d'
        self.btn_active = '#404040'
        self.accent = '#00d4aa'
        
        self.root.configure(bg=self.bg_color)
        self.vars = {}
        self.history = []
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🧮 Cyberxjn Calculator", 
                        font=('Arial', 18, 'bold'), 
                        fg=self.accent, bg=self.bg_color)
        title.pack(pady=10)
        
        # Display
        self.display = tk.Entry(self.root, font=('Consolas', 24, 'bold'),
                               justify='right', bg='#0f0f0f', fg=self.fg_color,
                               bd=0, insertbackground=self.fg_color,
                               relief='flat')
        self.display.pack(pady=20, padx=20, ipady=15, fill='x')
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Button layout
        buttons = [
            ('C', 1), ('±', 1), ('%', 1), ('÷', 1),
            ('7', 1), ('8', 1), ('9', 1), ('×', 1),
            ('4', 1), ('5', 1), ('6', 1), ('-', 1),
            ('1', 1), ('2', 1), ('3', 1), ('+', 1),
            ('0', 2), ('.', 1), ('=', 1)
        ]
        
        row, col = 0, 0
        for text, span in buttons:
            self.create_button(btn_frame, text, row, col, span)
            col += span
            if col >= 4:
                col = 0
                row += 1
        
        # Scientific buttons (top row)
        sci_frame = tk.Frame(self.root, bg=self.bg_color)
        sci_frame.pack(pady=5, padx=20, fill='x')
        
        sci_buttons = ['sin', 'cos', 'tan', 'log', '√', 'π']
        for i, text in enumerate(sci_buttons):
            btn = tk.Button(sci_frame, text=text, font=('Arial', 10),
                          bg=self.btn_bg, fg=self.fg_color, bd=0,
                          activebackground=self.btn_active,
                          command=lambda t=text: self.add_to_display(t))
            btn.pack(side='left', padx=2, pady=5, fill='x', expand=True)
        
        # History & Vars button
        bottom_frame = tk.Frame(self.root, bg=self.bg_color)
        bottom_frame.pack(pady=10, fill='x', padx=20)
        
        hist_btn = tk.Button(bottom_frame, text="📜 History", 
                           bg=self.accent, fg=self.bg_color, bd=0,
                           font=('Arial', 10, 'bold'),
                           command=self.show_history)
        hist_btn.pack(side='left', fill='x', expand=True, padx=(0,5))
        
        var_btn = tk.Button(bottom_frame, text="🔧 Vars", 
                          bg=self.btn_bg, fg=self.fg_color, bd=0,
                          font=('Arial', 10, 'bold'),
                          command=self.show_vars)
        var_btn.pack(side='right', fill='x', expand=True)
    
    def create_button(self, parent, text, row, col, colspan=1):
        btn = tk.Button(parent, text=text, font=('Arial', 16, 'bold'),
                       bg=self.btn_bg, fg=self.fg_color, bd=0,
                       activebackground=self.btn_active,
                       command=lambda: self.button_click(text))
        btn.grid(row=row, column=col, columnspan=colspan, padx=2, pady=2,
                sticky='nsew', ipadx=20, ipady=20)
        
        # Equal button special styling
        if text == '=':
            btn.configure(bg=self.accent, activebackground='#00aa88')
    
    def button_click(self, char):
        current = self.display.get()
        
        if char == 'C':
            self.display.delete(0, tk.END)
        elif char == '±':
            if current:
                if current.startswith('-'):
                    self.display.delete(0, 1)
                else:
                    self.display.insert(0, '-')
        elif char == '%':
            try:
                val = eval(current) / 100
                self.display.delete(0, tk.END)
                self.display.insert(0, str(val))
            except:
                pass
        elif char == '=':
            self.calculate()
        else:
            self.display.insert(tk.END, char)
    
    def add_to_display(self, text):
        current = self.display.get()
        if text == 'π':
            self.display.insert(tk.END, str(math.pi))
        elif text == '√':
            self.display.insert(tk.END, 'sqrt(')
        else:
            self.display.insert(tk.END, text + '(')
    
    def safe_eval(self, expr):
        """Safe math evaluation"""
        # Replace variables
        for name, val in self.vars.items():
            expr = re.sub(rf'\b{name}\b', str(val), expr)
        
        expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
        
        safe_names = {
            'math': math, 'sin': math.sin, 'cos': math.cos, 
            'tan': math.tan, 'log': math.log, 'sqrt': math.sqrt,
            'pi': math.pi, 'e': math.e, 'abs': abs
        }
        
        try:
            return float(eval(expr, {"__builtins__": {}}, safe_names))
        except:
            raise ValueError("Math error!")
    
    def calculate(self):
        try:
            expr = self.display.get()
            result = self.safe_eval(expr)
            
            self.history.append(f"{expr} = {result}")
            if len(self.history) > 50:
                self.history.pop(0)
            
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            
        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
    
    def show_history(self):
        hist_window = tk.Toplevel(self.root)
        hist_window.title("📜 History")
        hist_window.geometry("400x400")
        hist_window.configure(bg=self.bg_color)
        
        text = scrolledtext.ScrolledText(hist_window, bg='#0f0f0f', fg=self.fg_color,
                                       font=('Consolas', 12), wrap=tk.WORD)
        text.pack(pady=20, padx=20, fill='both', expand=True)
        
        for entry in self.history[-20:]:
            text.insert(tk.END, entry + "\n")
        text.config(state='disabled')
    
    def show_vars(self):
        var_window = tk.Toplevel(self.root)
        var_window.title("🔧 Variables")
        var_window.geometry("300x300")
        var_window.configure(bg=self.bg_color)
        
        frame = tk.Frame(var_window, bg=self.bg_color)
        frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        for name, val in self.vars.items():
            tk.Label(frame, text=f"{name} = {val}", 
                    fg=self.fg_color, bg=self.bg_color,
                    font=('Arial', 12)).pack(anchor='w')

def main():
    root = tk.Tk()
    app = CyberxjnCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
