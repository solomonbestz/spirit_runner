import pygame
import random
from dataclasses import dataclass

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ghost Runner")


@dataclass
class Transform:
    x: float
    y: float

@dataclass
class Orb:
    points: int



def main()->None:
    clock = pygame.time.Clock()

    player_image = pygame.image.load("assets/Player16x16.png").convert_alpha()
    player_image = pygame.transform.scale(player_image, (48, 48))

    player_transform = Transform(
        WIDTH // 2,
        HEIGHT // 2
    )

    player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
 
    orb_image = pygame.image.load("assets/orb_green.png").convert_alpha()
    orb_image = pygame.transform.scale(orb_image, (32, 32))


    orb_transform = Transform(
        random.randint(40, WIDTH - 40),
        random.randint(40, HEIGHT - 40)
    )

    orb_data = Orb(points=10)
    orb_rect = orb_image.get_rect(center=(orb_transform.x, orb_transform.y))

    coin_sound = pygame.mixer.Sound("assets/coin.wav")

    score = 0
    font = pygame.font.Font(None, 36)

    speed = 250

    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed * dt
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed * dt


        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= speed * dt

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed * dt

        player_rect.clamp_ip(screen.get_rect())

        if player_rect.colliderect(orb_rect):
            score += orb_data.points
            coin_sound.play()

            orb_transform.x = random.randint(40, WIDTH - 40)
            orb_transform.y = random.randint(40, HEIGHT - 40)
            orb_rect.center = (orb_transform.x, orb_transform.y)

        screen.fill((15, 15, 25))

        screen.blit(orb_image, orb_rect)
        screen.blit(player_image, player_rect)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
