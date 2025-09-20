# src/main.py
import tkinter as tk
from src.gui.main_window import MainWindow
from src.gui.admin_window import AdminWindow
from src.database import create_tables
from tkinter import ttk

def main():
    """
    Ponto de entrada da aplicação. Inicializa a janela principal da GUI.
    """
    create_tables() 
    
    root = tk.Tk()
    app = MainWindow(root)
    
    app.run()

if __name__ == "__main__":
    main()