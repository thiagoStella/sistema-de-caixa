# src/gui/main_window.py
import tkinter as tk
from tkinter import ttk # Importa o módulo de widgets "temáticos"
from tkinter import messagebox

class MainWindow:
    """
    Representa a janela principal da aplicação de sistema de caixa.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Caixa - Operador")
        self.root.geometry("800x600")

        # Configura as colunas para se expandirem
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Frame principal para o layout (pode ser usado para dividir a tela)
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Configura o frame para se expandir
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1) # A linha do Treeview vai se expandir

        # Widgets de entrada do produto (ID, Quantidade)
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        ttk.Label(self.input_frame, text="ID do Produto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.produto_id_entry = ttk.Entry(self.input_frame, width=15)
        self.produto_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.produto_id_entry.focus() # Foca no campo para digitar

        ttk.Label(self.input_frame, text="Quantidade:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.quantidade_entry = ttk.Entry(self.input_frame, width=15)
        self.quantidade_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Botões de ação
        self.button_frame = ttk.Frame(self.input_frame)
        self.button_frame.grid(row=0, column=4, padx=10)
        
        ttk.Button(self.button_frame, text="Adicionar", command=self.adicionar_item_a_venda).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Remover", command=self.remover_item_da_venda).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Finalizar", command=self.finalizar_venda).grid(row=0, column=2, padx=5)
        
        # Lista de itens da venda (Treeview)
        # O Treeview é perfeito para exibir dados em formato de tabela
        self.venda_treeview = ttk.Treeview(self.main_frame, columns=("id", "nome", "qtd", "subtotal"), show="headings")
        self.venda_treeview.heading("id", text="ID")
        self.venda_treeview.heading("nome", text="Produto")
        self.venda_treeview.heading("qtd", text="Qtd")
        self.venda_treeview.heading("subtotal", text="Subtotal")
        self.venda_treeview.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Label para mostrar o total da venda
        self.total_label = ttk.Label(self.main_frame, text="Total: R$ 0.00", font=("Arial", 16, "bold"))
        self.total_label.grid(row=2, column=1, sticky="e", padx=5, pady=10)
        
    def run(self):
        """
        Inicia o loop principal da interface gráfica.
        """
        self.root.mainloop()

    # MÉTODOS A SEREM IMPLEMENTADOS NA PRÓXIMA SPRINT
    def adicionar_item_a_venda(self):
        messagebox.showinfo("Aviso", "Funcionalidade de Adicionar ainda não conectada ao backend.")
        
    def remover_item_da_venda(self):
        messagebox.showinfo("Aviso", "Funcionalidade de Remover ainda não conectada ao backend.")
    
    def finalizar_venda(self):
        messagebox.showinfo("Aviso", "Funcionalidade de Finalizar ainda não conectada ao backend.")