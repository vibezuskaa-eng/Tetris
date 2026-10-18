import pygame

pygame.init()
rodando = True
pygame.display.set_caption("tetris")

janela = pygame.display.set_mode((500, 700))
b = {
    "quadrado1":pygame.Rect(50, 50, 50, 50),
    "cor_preta":(255, 255, 255)
    }
def abaixar(a):
    for abaixando in range(1, 10):
        a["quadrado1"] -= 50
        return a

while rodando == True:  
    janela.fill((0, 0, 0))

    pygame.draw.rect(janela, b["cor_preta"], b["quadrado1"])

    pygame.display.flip()

    abaixar(b)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
         
        if evento.type == pygame.KEYDOWN: 
            match evento.key:
                case pygame.K_d:
                    b["quadrado1"].x += 5
                case pygame.K_a:
                    b["quadrado1"].x -= 50
pygame.quit()



