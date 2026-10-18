import pygame

TAMANHO = 50
COLUNAS, LINHAS = 10, 14
LARGURA, ALTURA = COLUNAS * TAMANHO, LINHAS * TAMANHO  # 500 x 700

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CINZA = (40, 40, 40)

INTERVALO_QUEDA = 500  # milissegundos entre cada descida


def novo_bloco():
    return pygame.Rect((COLUNAS // 2) * TAMANHO, 0, TAMANHO, TAMANHO)


def posicao_valida(bloco, fixos):
    dentro_da_tela = bloco.left >= 0 and bloco.right <= LARGURA and bloco.bottom <= ALTURA
    return dentro_da_tela and bloco.collidelist(fixos) == -1


def tentar_mover(bloco, dx, dy, fixos):
    """Move o bloco se a nova posição for válida. Retorna True se moveu."""
    teste = bloco.move(dx, dy)
    if posicao_valida(teste, fixos):
        bloco.update(teste)
        return True
    return False


def desenhar(janela, atual, fixos):
    janela.fill(PRETO)

    # grade
    for x in range(0, LARGURA, TAMANHO):
        pygame.draw.line(janela, CINZA, (x, 0), (x, ALTURA))
    for y in range(0, ALTURA, TAMANHO):
        pygame.draw.line(janela, CINZA, (0, y), (LARGURA, y))

    # blocos
    for bloco in fixos:
        pygame.draw.rect(janela, BRANCO, bloco)
    pygame.draw.rect(janela, BRANCO, atual)

    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("Tetris")
    janela = pygame.display.set_mode((LARGURA, ALTURA))
    clock = pygame.time.Clock()

    EVENTO_QUEDA = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_QUEDA, INTERVALO_QUEDA)

    fixos = []
    atual = novo_bloco()
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == EVENTO_QUEDA:
                if not tentar_mover(atual, 0, TAMANHO, fixos):
                    # não conseguiu descer: fixa o bloco e cria outro
                    fixos.append(atual)
                    atual = novo_bloco()
                    if not posicao_valida(atual, fixos):
                        print("Game over!")
                        rodando = False

            elif evento.type == pygame.KEYDOWN:
                match evento.key:
                    case pygame.K_d | pygame.K_RIGHT:
                        tentar_mover(atual, TAMANHO, 0, fixos)
                    case pygame.K_a | pygame.K_LEFT:
                        tentar_mover(atual, -TAMANHO, 0, fixos)
                    case pygame.K_s | pygame.K_DOWN:
                        tentar_mover(atual, 0, TAMANHO, fixos)

        desenhar(janela, atual, fixos)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()