import random
import pygame

TAMANHO = 50
COLUNAS, LINHAS = 10, 14
LARGURA, ALTURA = COLUNAS * TAMANHO, LINHAS * TAMANHO  # 500 x 700

PRETO = (0, 0, 0)
CINZA = (40, 40, 40)

INTERVALO_QUEDA = 500  # ms

# As 7 peças clássicas (tetraminós): 1 = bloco, 0 = vazio
FORMAS = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1],
          [1, 1]],
    "T": [[0, 1, 0],
          [1, 1, 1]],
    "S": [[0, 1, 1],
          [1, 1, 0]],
    "Z": [[1, 1, 0],
          [0, 1, 1]],
    "J": [[1, 0, 0],
          [1, 1, 1]],
    "L": [[0, 0, 1],
          [1, 1, 1]],
}

# Cores padrão do Tetris
CORES = {
    "I": (0, 240, 240),   # ciano
    "O": (240, 240, 0),   # amarelo
    "T": (180, 0, 240),   # roxo
    "S": (0, 240, 0),     # verde
    "Z": (240, 0, 0),     # vermelho
    "J": (40, 110, 255),  # azul (mais claro para aparecer no fundo preto)
    "L": (240, 160, 0),   # laranja
}

class Peca:
    def __init__(self, nome):
        self.nome = nome
        self.forma = [linha[:] for linha in FORMAS[nome]]
        self.cor = CORES[nome]
        self.x = (COLUNAS - len(self.forma[0])) // 2
        self.y = 0

    def celulas(self, forma=None, x=None, y=None):
        """Retorna as posições (coluna, linha) ocupadas na grade."""
        forma = self.forma if forma is None else forma
        x = self.x if x is None else x
        y = self.y if y is None else y
        return [
            (x + c, y + l)
            for l, linha in enumerate(forma)
            for c, valor in enumerate(linha)
            if valor
        ]

    def forma_girada(self):
        # rotação de 90° no sentido horário
        return [list(linha) for linha in zip(*self.forma[::-1])]


def sorteador():
    """Gera peças em 'sacos' de 7, para todas aparecerem com frequência parecida."""
    while True:
        saco = list(FORMAS)
        random.shuffle(saco)
        for nome in saco:
            yield Peca(nome)


def posicao_valida(grade, celulas):
    for c, l in celulas:
        # l < 0 também é inválido: a peça nunca pode ficar acima do tabuleiro
        if c < 0 or c >= COLUNAS or l < 0 or l >= LINHAS:
            return False
        if grade[l][c] is not None:
            return False
    return True


def mover(grade, peca, dx, dy):
    if posicao_valida(grade, peca.celulas(x=peca.x + dx, y=peca.y + dy)):
        peca.x += dx
        peca.y += dy
        return True
    return False


def girar(grade, peca):
    nova = peca.forma_girada()
    # tenta girar; se bater na parede/chão/outras peças, tenta deslocar a peça
    for dy in (0, -1, -2, -3):
        for dx in (0, -1, 1, -2, 2):
            celulas = peca.celulas(forma=nova, x=peca.x + dx, y=peca.y + dy)
            if posicao_valida(grade, celulas):
                peca.forma = nova
                peca.x += dx
                peca.y += dy
                return


def fixar(grade, peca):
    for c, l in peca.celulas():
        grade[l][c] = peca.cor


def limpar_linhas(grade):
    cheias = [i for i, linha in enumerate(grade) if all(c is not None for c in linha)]
    for i in cheias:
        del grade[i]
        grade.insert(0, [None] * COLUNAS)
    return len(cheias)


def desenhar_bloco(janela, cor, c, l):
    rect = pygame.Rect(c * TAMANHO, l * TAMANHO, TAMANHO, TAMANHO)
    pygame.draw.rect(janela, cor, rect)
    pygame.draw.rect(janela, PRETO, rect, 2)  # borda


def desenhar(janela, grade, peca):
    janela.fill(PRETO)

    for x in range(0, LARGURA, TAMANHO):
        pygame.draw.line(janela, CINZA, (x, 0), (x, ALTURA))
    for y in range(0, ALTURA, TAMANHO):
        pygame.draw.line(janela, CINZA, (0, y), (LARGURA, y))

    for l, linha in enumerate(grade):
        for c, cor in enumerate(linha):
            if cor is not None:
                desenhar_bloco(janela, cor, c, l)

    for c, l in peca.celulas():
        desenhar_bloco(janela, peca.cor, c, l)

    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("Tetris")
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    clock = pygame.time.Clock()

    EVENTO_QUEDA = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_QUEDA, INTERVALO_QUEDA)

    grade = [[None] * COLUNAS for _ in range(LINHAS)]
    pecas = sorteador()
    atual = next(pecas)
    proxima = next(pecas)
    pontos = 0
    pygame.display.set_caption(f"Tetris - atual: {atual.nome} | próxima: {proxima.nome}")
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == EVENTO_QUEDA:
                if not mover(grade, atual, 0, 1):
                    fixar(grade, atual)
                    pontos += limpar_linhas(grade) * 100
                    atual, proxima = proxima, next(pecas)
                    pygame.display.set_caption(f"Tetris - atual: {atual.nome} | próxima: {proxima.nome}")
                    if not posicao_valida(grade, atual.celulas()):
                        print(f"Game over! Pontos: {pontos}")
                        rodando = False

            elif evento.type == pygame.KEYDOWN:
                match evento.key:
                    case pygame.K_d | pygame.K_RIGHT:
                        mover(grade, atual, 1, 0)      # right
                    case pygame.K_a | pygame.K_LEFT:
                        mover(grade, atual, -1, 0)     # left
                    case pygame.K_s | pygame.K_DOWN:
                        mover(grade, atual, 0, 1)      # down one row
                    case pygame.K_w | pygame.K_UP:
                        girar(grade, atual)            # rotate
                    case pygame.K_SPACE:
                        while mover(grade, atual, 0, 1):   # instant drop (space bar)
                            pass
        desenhar(janela, grade, atual)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()