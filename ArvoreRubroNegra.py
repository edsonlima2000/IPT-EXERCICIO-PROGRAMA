"""
Implementacao completa de uma arvore rubro-negra com operacoes de
insercao, busca, remocao e impressao bidimensional.

Executa uma interface grafica simples (Tkinter) para inserir, buscar e
remover elementos.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional


RED = "RED"
BLACK = "BLACK"


class No:
    """No da arvore rubro-negra. Nunca usa None; usa sentinela NIL."""

    __slots__ = ("chave", "cor", "esquerda", "direita", "pai")

    def __init__(self, chave: int, cor: str = RED) -> None:
        self.chave: int = chave
        self.cor: str = cor
        self.esquerda: No = self
        self.direita: No = self
        self.pai: No = self

    def __repr__(self) -> str:
        return f"{self.chave}({self.cor[0]})"


class ArvoreRubroNegra:
    """Arvore rubro-negra baseada no algoritmo do CLRS."""

    def __init__(self) -> None:
        self.nil = No(chave=0, cor=BLACK)  # sentinela
        self.nil.esquerda = self.nil.direita = self.nil.pai = self.nil
        self.raiz: No = self.nil

    # ----------------- Operacoes basicas -----------------
    def _rotacao_esquerda(self, x: No) -> None:
        y = x.direita
        x.direita = y.esquerda
        if y.esquerda is not self.nil:
            y.esquerda.pai = x
        y.pai = x.pai
        if x.pai is self.nil:
            self.raiz = y
        elif x is x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y

    def _rotacao_direita(self, y: No) -> None:
        x = y.esquerda
        y.esquerda = x.direita
        if x.direita is not self.nil:
            x.direita.pai = y
        x.pai = y.pai
        if y.pai is self.nil:
            self.raiz = x
        elif y is y.pai.direita:
            y.pai.direita = x
        else:
            y.pai.esquerda = x
        x.direita = y
        y.pai = x

    # ----------------- Insercao -----------------
    def inserir(self, chave: int) -> None:
        """Insere uma chave na arvore e corrige as cores/rotacoes."""
        novo = No(chave=chave, cor=RED)
        novo.esquerda = self.nil
        novo.direita = self.nil
        novo.pai = self.nil
        y = self.nil
        x = self.raiz
        while x is not self.nil:
            y = x
            if novo.chave < x.chave:
                x = x.esquerda
            else:
                x = x.direita
        novo.pai = y
        if y is self.nil:
            self.raiz = novo
        elif novo.chave < y.chave:
            y.esquerda = novo
        else:
            y.direita = novo
        self._corrigir_insercao(novo)

    def _corrigir_insercao(self, z: No) -> None:
        while z.pai.cor == RED:
            if z.pai is z.pai.pai.esquerda:
                tio = z.pai.pai.direita
                if tio.cor == RED:
                    z.pai.cor = BLACK
                    tio.cor = BLACK
                    z.pai.pai.cor = RED
                    z = z.pai.pai
                else:
                    if z is z.pai.direita:
                        z = z.pai
                        self._rotacao_esquerda(z)
                    z.pai.cor = BLACK
                    z.pai.pai.cor = RED
                    self._rotacao_direita(z.pai.pai)
            else:
                tio = z.pai.pai.esquerda
                if tio.cor == RED:
                    z.pai.cor = BLACK
                    tio.cor = BLACK
                    z.pai.pai.cor = RED
                    z = z.pai.pai
                else:
                    if z is z.pai.esquerda:
                        z = z.pai
                        self._rotacao_direita(z)
                    z.pai.cor = BLACK
                    z.pai.pai.cor = RED
                    self._rotacao_esquerda(z.pai.pai)
        self.raiz.cor = BLACK

    # ----------------- Busca -----------------
    def buscar(self, chave: int) -> Optional[No]:
        """Retorna o no com a chave, ou None se nao existir."""
        atual = self.raiz
        while atual is not self.nil:
            if chave == atual.chave:
                return atual
            if chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    # ----------------- Remocao -----------------
    def remover(self, chave: int) -> bool:
        """Remove a chave e retorna True se removida."""
        z = self.buscar(chave)
        if z is None:
            return False

        y = z
        y_cor_original = y.cor
        if z.esquerda is self.nil:
            x = z.direita
            self._transplantar(z, z.direita)
        elif z.direita is self.nil:
            x = z.esquerda
            self._transplantar(z, z.esquerda)
        else:
            y = self._minimo(z.direita)
            y_cor_original = y.cor
            x = y.direita
            if y.pai is z:
                x.pai = y
            else:
                self._transplantar(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y
            self._transplantar(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor
        if y_cor_original == BLACK:
            self._corrigir_remocao(x)
        return True

    def _transplantar(self, u: No, v: No) -> None:
        if u.pai is self.nil:
            self.raiz = v
        elif u is u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def _minimo(self, no: No) -> No:
        while no.esquerda is not self.nil:
            no = no.esquerda
        return no

    def _corrigir_remocao(self, x: No) -> None:
        while x is not self.raiz and x.cor == BLACK:
            if x is x.pai.esquerda:
                w = x.pai.direita
                if w.cor == RED:
                    w.cor = BLACK
                    x.pai.cor = RED
                    self._rotacao_esquerda(x.pai)
                    w = x.pai.direita
                if w.esquerda.cor == BLACK and w.direita.cor == BLACK:
                    w.cor = RED
                    x = x.pai
                else:
                    if w.direita.cor == BLACK:
                        w.esquerda.cor = BLACK
                        w.cor = RED
                        self._rotacao_direita(w)
                        w = x.pai.direita
                    w.cor = x.pai.cor
                    x.pai.cor = BLACK
                    w.direita.cor = BLACK
                    self._rotacao_esquerda(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esquerda
                if w.cor == RED:
                    w.cor = BLACK
                    x.pai.cor = RED
                    self._rotacao_direita(x.pai)
                    w = x.pai.esquerda
                if w.direita.cor == BLACK and w.esquerda.cor == BLACK:
                    w.cor = RED
                    x = x.pai
                else:
                    if w.esquerda.cor == BLACK:
                        w.direita.cor = BLACK
                        w.cor = RED
                        self._rotacao_esquerda(w)
                        w = x.pai.esquerda
                    w.cor = x.pai.cor
                    x.pai.cor = BLACK
                    w.esquerda.cor = BLACK
                    self._rotacao_direita(x.pai)
                    x = self.raiz
        x.cor = BLACK

    # ----------------- Impressao -----------------
    def _desenhar(self, no: No, prefixo: str, eh_esquerda: bool, saida: List[str]) -> None:
        if no is self.nil:
            return
        conector = "+--"
        saida.append(f"{prefixo}{conector}{no.chave} ({'V' if no.cor == RED else 'P'})")
        prox_prefixo = f"{prefixo}{'   ' if eh_esquerda else '|  '}"
        self._desenhar(no.direita, prox_prefixo, False, saida)
        self._desenhar(no.esquerda, prox_prefixo, True, saida)

    def visualizar(self) -> str:
        """Retorna uma string com a arvore desenhada na vertical."""
        if self.raiz is self.nil:
            return "(arvore vazia)"
        linhas: List[str] = [f"{self.raiz.chave} ({'V' if self.raiz.cor == RED else 'P'})"]
        self._desenhar(self.raiz.direita, "", False, linhas)
        self._desenhar(self.raiz.esquerda, "", True, linhas)
        return "\n".join(linhas)

    # ----------------- Utilidades -----------------
    def inorder(self) -> List[int]:
        def _in(no: No):
            if no is self.nil:
                return
            yield from _in(no.esquerda)
            yield no.chave
            yield from _in(no.direita)

        return list(_in(self.raiz))


def executar_interface_visual() -> None:
    """Interface grafica simples com botoes e desenho em canvas."""
    arvore = ArvoreRubroNegra()

    root = tk.Tk()
    root.title("Arvore Rubro-Negra")
    root.geometry("900x600")

    status_var = tk.StringVar(value="Pronto.")

    frame_controles = ttk.Frame(root, padding=10)
    frame_controles.pack(fill="x")

    ttk.Label(frame_controles, text="Valor (inteiro):").pack(side="left")
    entrada_valor = ttk.Entry(frame_controles, width=10)
    entrada_valor.pack(side="left", padx=5)

    def obter_valor() -> Optional[int]:
        texto = entrada_valor.get().strip()
        if not texto:
            messagebox.showinfo("Aviso", "Informe um valor inteiro.")
            return None
        try:
            return int(texto)
        except ValueError:
            messagebox.showerror("Erro", "Valor invalido. Use apenas inteiros.")
            return None

    canvas = tk.Canvas(root, bg="white", height=350)
    canvas.pack(fill="both", expand=True, padx=10, pady=10)

    quadro_texto = tk.Text(root, height=12, wrap="none")
    quadro_texto.pack(fill="both", expand=False, padx=10, pady=(0, 10))
    quadro_texto.configure(state="disabled")

    ttk.Label(root, textvariable=status_var, anchor="w").pack(fill="x", padx=10, pady=(0, 10))

    def atualizar_texto() -> None:
        quadro_texto.configure(state="normal")
        quadro_texto.delete("1.0", tk.END)
        quadro_texto.insert(tk.END, arvore.visualizar())
        quadro_texto.configure(state="disabled")

    def layout_nos():
        pos = {}
        contador = 0
        margem_x = 30
        margem_y = 40
        espacamento_x = 60
        espacamento_y = 80

        def inorder(no: No, profundidade: int) -> None:
            nonlocal contador
            if no is arvore.nil:
                return
            inorder(no.esquerda, profundidade + 1)
            x = margem_x + contador * espacamento_x
            y = margem_y + profundidade * espacamento_y
            pos[no] = (x, y)
            contador += 1
            inorder(no.direita, profundidade + 1)

        inorder(arvore.raiz, 0)
        return pos

    def desenhar_arvore() -> None:
        canvas.delete("all")
        pos = layout_nos()
        if not pos:
            return
        # Ajusta largura do canvas conforme numero de nos
        largura_minima = 600
        largura_calculada = max(largura_minima, len(pos) * 60)
        canvas.config(scrollregion=(0, 0, largura_calculada, 600))
        raio = 20
        for no, (x, y) in pos.items():
            if no.esquerda is not arvore.nil:
                xe, ye = pos[no.esquerda]
                canvas.create_line(x, y, xe, ye, fill="gray30", width=2)
            if no.direita is not arvore.nil:
                xd, yd = pos[no.direita]
                canvas.create_line(x, y, xd, yd, fill="gray30", width=2)
        for no, (x, y) in pos.items():
            fill = "#c0392b" if no.cor == RED else "#2c3e50"
            texto_cor = "white"
            canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill=fill, outline="black", width=2)
            canvas.create_text(x, y, text=str(no.chave), fill=texto_cor, font=("Segoe UI", 10, "bold"))

    def acao_inserir() -> None:
        valor = obter_valor()
        if valor is None:
            return
        arvore.inserir(valor)
        status_var.set(f"Valor {valor} inserido.")
        atualizar_texto()
        desenhar_arvore()

    def acao_buscar() -> None:
        valor = obter_valor()
        if valor is None:
            return
        encontrado = arvore.buscar(valor)
        if encontrado:
            status_var.set(f"Encontrado: {valor} ({'V' if encontrado.cor == RED else 'P'}).")
        else:
            status_var.set("Valor nao encontrado.")
        atualizar_texto()
        desenhar_arvore()

    def acao_remover() -> None:
        valor = obter_valor()
        if valor is None:
            return
        if arvore.remover(valor):
            status_var.set(f"Valor {valor} removido.")
        else:
            status_var.set("Valor nao encontrado para remocao.")
        atualizar_texto()
        desenhar_arvore()

    botoes = ttk.Frame(frame_controles)
    botoes.pack(side="left", padx=10)
    ttk.Button(botoes, text="Inserir", command=acao_inserir).pack(side="left", padx=2)
    ttk.Button(botoes, text="Buscar", command=acao_buscar).pack(side="left", padx=2)
    ttk.Button(botoes, text="Remover", command=acao_remover).pack(side="left", padx=2)

    atualizar_texto()
    desenhar_arvore()
    root.mainloop()


if __name__ == "__main__":
    executar_interface_visual()
