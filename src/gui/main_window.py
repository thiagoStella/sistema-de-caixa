# src/gui/main_window.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.gui.admin_window import AdminWindow

# Importa as classes e repositórios do backend
from src.models import Produto, Venda, ItemVenda
from src.repository import ProdutoRepository, VendaRepository

class MainWindow:
    """
    Representa a janela principal da aplicação de sistema de caixa.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Caixa - Operador")
        self.root.geometry("800x600")

        # Inicializa a venda em andamento e os repositórios
        self.venda_atual = Venda()
        self.produto_repo = ProdutoRepository()
        self.venda_repo = VendaRepository()

        # Configura as colunas para se expandirem
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Frame principal para o layout (pode ser usado para dividir a tela)
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        # Widgets de entrada do produto (ID, Quantidade)
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        ttk.Label(self.input_frame, text="Nome do Produto:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.produto_id_entry = ttk.Entry(self.input_frame, width=15)
        self.produto_id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.produto_id_entry.focus()

        ttk.Label(self.input_frame, text="Quantidade:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.quantidade_entry = ttk.Entry(self.input_frame, width=15)
        self.quantidade_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Botões de ação
        self.button_frame = ttk.Frame(self.input_frame)
        self.button_frame.grid(row=0, column=4, padx=10)
        
        ttk.Button(self.button_frame, text="Adicionar", command=self.adicionar_item_a_venda).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Remover", command=self.remover_item_da_venda).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Finalizar", command=self.finalizar_venda).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Administrador", command=lambda: AdminWindow(self.root)).grid(row=0, column=3, padx=5)
        
        # Lista de itens da venda (Treeview)
        self.venda_treeview = ttk.Treeview(self.main_frame, columns=("id", "nome", "qtd", "subtotal"), show="headings")
        self.venda_treeview.heading("id", text="ID")
        self.venda_treeview.heading("nome", text="Produto")
        self.venda_treeview.heading("qtd", text="Qtd")
        self.venda_treeview.heading("subtotal", text="Subtotal")
        self.venda_treeview.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Label para mostrar o total da venda
        self.total_label = ttk.Label(self.main_frame, text="Total: R$ 0.00", font=("Arial", 16, "bold"))
        self.total_label.grid(row=2, column=1, sticky="e", padx=5, pady=10)

        # Define os métodos
    def adicionar_item_a_venda(self):
        try:
            # Obtém o nome e a quantidade do produto
            produto_nome = self.produto_id_entry.get().strip()
            quantidade = float(self.quantidade_entry.get().replace(',', '.'))
        except (ValueError, tk.TclError):
            messagebox.showerror("Erro de entrada", "Por favor, insira um nome e uma quantidade válidos.")
            return

        produto_selecionado = self.produto_repo.get_by_name(produto_nome)
        if not produto_selecionado:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        try:
            if quantidade <= 0 or quantidade > produto_selecionado.estoque:
                raise ValueError("Quantidade inválida ou insuficiente em estoque.")
            
            item_venda = ItemVenda(
                produto=produto_selecionado, 
                quantidade=quantidade,
                preco_unitario_na_venda=produto_selecionado.preco
            )
            
            self.venda_atual.adicionar_item(item_venda)
            self.update_item_list()
            self.update_total()

            self.produto_id_entry.delete(0, tk.END)
            self.quantidade_entry.delete(0, tk.END)
            self.produto_id_entry.focus()
            
        except ValueError as e:
            messagebox.showerror("Erro de lógica", str(e))
    
    def remover_item_da_venda(self):
        selected_item = self.venda_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return

        # Pega o ID do item da venda selecionado
        item_data = self.venda_treeview.item(selected_item, "values")
        item_id_do_treeview = item_data[0]
        
        # Remove o item da lista em memória da venda atual
        self.venda_atual.itens = [item for item in self.venda_atual.itens if str(item.produto.id) != item_id_do_treeview]
        self.venda_atual.total = sum(item.subtotal for item in self.venda_atual.itens)

        self.update_item_list()
        self.update_total()

    def finalizar_venda(self):
        if not self.venda_atual or not self.venda_atual.itens:
            messagebox.showwarning("Aviso", "Não há itens para finalizar a compra.")
            return

        try:
            # Salva a venda no banco de dados
            self.venda_repo.save(self.venda_atual)
            
            # Atualiza o estoque de cada produto no banco de dados
            for item in self.venda_atual.itens:
                produto_db = self.produto_repo.get_by_id(item.produto.id)
                if produto_db:
                    produto_db.atualizar_estoque(-item.quantidade)
                    self.produto_repo.save(produto_db)
            
            messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")

            # Reinicia a venda para uma nova transação
            self.venda_atual = Venda()
            self.update_item_list()
            self.update_total()

        except Exception as e:
            messagebox.showerror("Erro na finalização", f"Ocorreu um erro ao finalizar a venda: {e}")

    def update_item_list(self):
        # Limpa o Treeview antes de preencher
        for item in self.venda_treeview.get_children():
            self.venda_treeview.delete(item)

        # Adiciona os itens da venda atual ao Treeview
        for item in self.venda_atual.itens:
            self.venda_treeview.insert("", "end", values=(
                item.produto.id, 
                item.produto.nome, 
                item.quantidade, 
                f"R${item.subtotal:.2f}"
            ))

    def update_total(self):
        # Atualiza o rótulo do total
        self.total_label.config(text=f"Total: R$ {self.venda_atual.total:.2f}")

    def run(self):
        """
        Inicia o loop principal da interface gráfica.
        """
        self.root.mainloop()