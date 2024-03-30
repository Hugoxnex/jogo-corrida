import pygame
import random
import sys

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Classes
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/home/xnex/Downloads/jogo/download.jpeg").convert()  # Carregar imagem do carro
        self.image = pygame.transform.scale(self.image, (50, 30))  # Redimensionar imagem
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speed = 0

    def update(self):
        # Controle do carro
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed += 0.5
        if keys[pygame.K_DOWN]:
            self.speed -= 0.5
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Limites da tela (teleporte)
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

        # Movimento do carro
        self.rect.y += self.speed

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((30, 30))  # Retângulo representando o obstáculo
        self.image.fill(color)  # Cor
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += 5

        # Se o obstáculo sair da tela, ele é reposicionado no topo
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = -self.rect.height

# Função para desenhar texto na tela
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)  # Mudança para o canto superior esquerdo
    surface.blit(text_surface, text_rect)

# Função principal
def main():
    # Inicialização
    pygame.init()

    # Carregar a imagem de fundo
    background = pygame.image.load("/home/xnex/Downloads/jogo/jogos-de-corrida-para-android.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Configuração da tela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jogo de Corrida Aprimorado")

    # Criação dos sprites
    car = Car()
    obstacle_yellow = Obstacle(YELLOW)
    obstacle_green = Obstacle(GREEN)

    # Grupo de sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(car)
    all_sprites.add(obstacle_yellow)
    all_sprites.add(obstacle_green)

    # Variáveis de controle
    score = 0
    time = 0

    # Fonte para o texto
    font = pygame.font.Font(None, 36)

    # Contador de tempo
    start_time = pygame.time.get_ticks()
    game_over = False
    restart_time = None

    # Loop principal
    clock = pygame.time.Clock()
    running = True
    while running:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualização dos sprites
        if not game_over:
            all_sprites.update()

            # Verificar colisão entre o carro e os obstáculos
            collisions = pygame.sprite.spritecollide(car, all_sprites, False)
            if collisions:
                for obstacle in collisions:
                    if isinstance(obstacle, Obstacle):  # Verificar se o objeto é uma instância de Obstacle
                        if obstacle.color == YELLOW:
                            game_over = True  # Sinalizar que o jogo acabou
                            restart_time = pygame.time.get_ticks()
                            game_over_text = "Você bateu no obstáculo amarelo! Pressione R para reiniciar ou Q para sair."
                        elif obstacle.color == GREEN:
                            score += 1  # Incrementar a pontuação se colidir com o obstáculo verde
                            obstacle.rect.y = -obstacle.rect.height  # Reposicionar o obstáculo no topo
                            obstacle.rect.x = random.randint(0, SCREEN_WIDTH - obstacle.rect.width)

                            # Verificar marcos de pontuação
                            if score == 10 or score == 20 or score == 30:
                                milestone_text = "PARABÉNS! Você atingiu " + str(score) + " pontos!"
                            elif score == 40:
                                milestone_text = "AI SIM! VOCÊ ESTÁ FICANDO BOM!"

            # Contador de tempo
            current_time = pygame.time.get_ticks()
            time_elapsed = (current_time - start_time) // 1000  # Converter para segundos

        # Desenhar elementos na tela
        screen.blit(background, (0, 0))  # Desenhar o fundo
        all_sprites.draw(screen)
        draw_text(screen, "Pontuação: " + str(score), font, WHITE, 10, 10)
        draw_text(screen, "Tempo: " + str(time_elapsed), font, WHITE, 10, 50)

        # Exibir mensagem de fim de jogo, se aplicável
        if game_over:
            draw_text(screen, game_over_text, font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Exibir mensagem de marco de pontuação, se aplicável
        if score in [10, 20, 30, 40]:
            draw_text(screen, milestone_text, font, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        # Atualizar a tela
        pygame.display.flip()

        # Controle de velocidade
        clock.tick(60)

        # Eventos de reinicialização do jogo
        keys = pygame.key.get_pressed()
        if game_over:
            if keys[pygame.K_r]:  # Reiniciar jogo
                main()
            elif keys[pygame.K_q]:  # Sair do jogo
                pygame.quit()
                sys.exit()

    pygame.quit()

if __name__ == "__main__":
    main()
