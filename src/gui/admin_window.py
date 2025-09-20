# src/gui/admin_window.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from src.models import Produto
from src.repository import ProdutoRepository

class AdminWindow(tk.Toplevel):
    """
    Representa a janela administrativa para o dono gerenciar os produtos.
    """
    def __init__(self, master):
        super().__init__(master)
        self.title("Modo Administrativo - Gerenciar Produtos")
        self.geometry("600x450")
        
        self.transient(master)
        
        self.produto_repo = ProdutoRepository()

        # Frame de login
        self.login_frame = ttk.Frame(self, padding="20")
        self.login_frame.pack(expand=True)
        
        ttk.Label(self.login_frame, text="Digite a senha de acesso:").pack(pady=5)
        self.senha_entry = ttk.Entry(self.login_frame, show="*", width=20)
        self.senha_entry.pack(pady=5)
        self.senha_entry.bind("<Return>", lambda event: self.check_password())
        
        ttk.Button(self.login_frame, text="Entrar", command=self.check_password).pack(pady=5)

    def check_password(self):
        senha = self.senha_entry.get()
        SENHA_ADMIN = "admin123"
        
        if senha == SENHA_ADMIN:
            self.login_frame.destroy()
            self.setup_admin_panel()
        else:
            messagebox.showerror("Erro de Senha", "Senha incorreta. Acesso negado.")
            self.senha_entry.delete(0, tk.END)

    def setup_admin_panel(self):
        self.admin_frame = ttk.Frame(self, padding="10")
        self.admin_frame.pack(fill="both", expand=True)
        
        self.button_frame = ttk.Frame(self.admin_frame)
        self.button_frame.pack(pady=10)
        
        ttk.Button(self.button_frame, text="Adicionar Produto", command=self.add_product_form).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Editar Produto", command=self.edit_product_form).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Deletar Produto", command=self.delete_product).pack(side="left", padx=5)

        self.product_treeview = ttk.Treeview(self.admin_frame, columns=("id", "nome", "preco", "estoque"), show="headings")
        self.product_treeview.heading("id", text="ID")
        self.product_treeview.heading("nome", text="Nome")
        self.product_treeview.heading("preco", text="Preço")
        self.product_treeview.heading("estoque", text="Estoque")
        
        self.product_treeview.column("id", width=50, anchor="center")
        self.product_treeview.column("preco", width=100, anchor="center")
        self.product_treeview.column("estoque", width=100, anchor="center")
        
        self.product_treeview.pack(fill="both", expand=True, pady=10)
        self.display_products_in_treeview()

    def display_products_in_treeview(self):
        for item in self.product_treeview.get_children():
            self.product_treeview.delete(item)
        
        produtos = self.produto_repo.get_all()
        for p in produtos:
            self.product_treeview.insert("", "end", values=(p.id, p.nome, f"R${p.preco:.2f}", p.estoque))

    def add_product_form(self):
        # Janela pop-up para adicionar produto
        add_win = tk.Toplevel(self)
        add_win.title("Adicionar Novo Produto")
        add_win.geometry("500x300")

        ttk.Label(add_win, text="Nome:").pack(pady=5)
        name_entry = ttk.Entry(add_win)
        name_entry.pack(pady=5)
        
        ttk.Label(add_win, text="Preço:").pack(pady=5)
        price_entry = ttk.Entry(add_win)
        price_entry.pack(pady=5)

        ttk.Label(add_win, text="Estoque:").pack(pady=5)
        stock_entry = ttk.Entry(add_win)
        stock_entry.pack(pady=5)

        def save():
            try:
                nome = name_entry.get().strip()
                preco = float(price_entry.get().replace(',', '.'))
                estoque = int(stock_entry.get())

                if not nome or preco <= 0 or estoque < 0:
                    messagebox.showerror("Erro", "Campos inválidos. Por favor, preencha corretamente.")
                    return
                
                # Assume tipo_unidade como 'UNIDADE' para simplificar o formulário
                novo_produto = Produto(nome=nome, preco=preco, tipo_unidade="UNIDADE", estoque=estoque)
                self.produto_repo.save(novo_produto)
                self.display_products_in_treeview()
                add_win.destroy()
                messagebox.showinfo("Sucesso", "Produto adicionado!")
            except ValueError:
                messagebox.showerror("Erro", "Preço ou estoque devem ser números válidos.")

        ttk.Button(add_win, text="Salvar", command=save).pack(pady=10)

    def edit_product_form(self):
        selected_item = self.product_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um produto para editar.")
            return

        item_data = self.product_treeview.item(selected_item, "values")
        produto_id = item_data[0]
        produto = self.produto_repo.get_by_id(produto_id)

        edit_win = tk.Toplevel(self)
        edit_win.title(f"Editar Produto: {produto.nome}")
        edit_win.geometry("500x300")
        
        ttk.Label(edit_win, text="Nome:").pack(pady=5)
        name_entry = ttk.Entry(edit_win)
        name_entry.insert(0, produto.nome)
        name_entry.pack(pady=5)
        
        ttk.Label(edit_win, text="Preço:").pack(pady=5)
        price_entry = ttk.Entry(edit_win)
        price_entry.insert(0, produto.preco)
        price_entry.pack(pady=5)

        ttk.Label(edit_win, text="Estoque:").pack(pady=5)
        stock_entry = ttk.Entry(edit_win)
        stock_entry.insert(0, produto.estoque)
        stock_entry.pack(pady=5)

        def save_edit():
            try:
                produto.nome = name_entry.get().strip()
                produto.preco = float(price_entry.get().replace(',', '.'))
                produto.estoque = int(stock_entry.get())
                
                self.produto_repo.save(produto)
                self.display_products_in_treeview()
                edit_win.destroy()
                messagebox.showinfo("Sucesso", "Produto editado com sucesso!")
            except ValueError:
                messagebox.showerror("Erro", "Preço ou estoque devem ser números válidos.")

        ttk.Button(edit_win, text="Salvar Alterações", command=save_edit).pack(pady=10)

    def delete_product(self):
        selected_item = self.product_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um produto para deletar.")
            return

        item_data = self.product_treeview.item(selected_item, "values")
        produto_id = item_data[0]
        produto_nome = item_data[1]
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o produto '{produto_nome}'?"):
            if self.produto_repo.delete(produto_id):
                messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
                self.display_products_in_treeview()
            else:
                messagebox.showerror("Erro", "Não foi possível deletar o produto.")