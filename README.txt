Exercicio-Programa 1 - Arvore Rubro-Negra
------------------------------------------

Conteudo:
- Implementacao completa de uma arvore rubro-negra (CLRS) em Python.
- Interface grafica (Tkinter) para inserir, buscar e remover chaves.
- Visualizacao em ASCII (quadro de texto) e desenho em canvas com cores.

Requisitos:
- Python 3.12 (testado no Windows 10).
- Tkinter (vem na instalacao padrao do Python no Windows).

Preparar ambiente (recomendado):
1) Criar/ativar ambiente virtual:
   python -m venv .venv
   .\\.venv\\Scripts\\Activate

2) Dependencias: apenas biblioteca padrao (Tkinter).

Como executar (GUI):
1) Ative o ambiente virtual (opcional, se criado).
2) Rode: python ArvoreRubroNegra.py
3) Use o campo de valor inteiro e os botoes:
   - Inserir: insere a chave (cor vermelha, corrigida para manter propriedades).
   - Buscar: procura a chave e atualiza a mensagem de status.
   - Remover: remove a chave, se existir.
   O quadro inferior mostra a arvore em ASCII; o canvas desenha a arvore com nos vermelhos/preto.

Exemplo rapido (GUI):
- Inserir: 10, 5, 40
- Buscar: 5
- Remover: 10

Teste programatico simples (fora da GUI):
from ArvoreRubroNegra import ArvoreRubroNegra
arv = ArvoreRubroNegra()
for v in [10,5,1,7,40,50]:
    arv.inserir(v)
print(arv.inorder())          # [1, 5, 7, 10, 40, 50]
arv.remover(40)
print(arv.inorder())          # [1, 5, 7, 10, 50]

Notas de implementacao:
- Usa sentinela NIL (nunca None) para simplificar correcoes.
- As operacoes de insercao/remocao seguem o algoritmo do CLRS.
- A impressao ASCII omite NILs; o canvas colore nos vermelhos (#c0392b) e pretos (#2c3e50).
