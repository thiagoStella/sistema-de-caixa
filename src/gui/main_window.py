# src/gui/main_window.py
import tkinter as tk

class MainWindow:
    """
    Representa a janela principal da aplicação de sistema de caixa.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Caixa - Operador")
        self.root.geometry("800x600")
        
        # Aqui, no futuro, vamos adicionar os widgets (botões, labels, etc.)

        print("Janela principal da GUI criada com sucesso.")

    def run(self):
        """
        Inicia o loop principal da interface gráfica.
        """
        self.root.mainloop()