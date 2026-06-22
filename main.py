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


@dataclass
class Collectible:
    image: pygame.Surface
    transform: Transform
    orb: Orb
    rect: pygame.Rect


@dataclass
class Animation:
    frames: list[pygame.Surface]
    frame_index: int
    timer: float
    frame_duration: float

@dataclass
class Ghost:
    image: pygame.Surface
    transform: Transform
    rect: pygame.Rect
    mask: pygame.mask.Mask
    speed: float


def load_animation_frames(
        path: str,
        frame_width: int,
        frame_height: int,
        scale: int,
        row: int,
        frame_count: int,
) -> list[pygame.Surface]:
    sheet = pygame.image.load(path).convert_alpha()

    frames = []

    for index in range(frame_count):
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

        frame.blit(
            sheet,
            (0, 0),
            (
                index * frame_width,
                row * frame_height,
                frame_width,
                frame_height,
            )
        )

        frame = pygame.transform.scale(
            frame,
            (frame_width * scale, frame_height * scale),
        )
        frames.append(frame)
    return frames


def create_orb(image_path: str, points: int) -> Collectible:
    image = pygame.image.load(image_path).convert_alpha()
    image = pygame.transform.scale(image, (32, 32))

    transform = Transform(
        random.randint(40, WIDTH - 40),
        random.randint(40, HEIGHT - 40)
    )

    rect = image.get_rect(center=(transform.x, transform.y))

    return Collectible(
        image=image,
        transform=transform,
        orb=Orb(points=points),
        rect=rect,
    )


def create_ghost()-> Ghost:
    image = pygame.image.load("assets/ghost_v2.png").convert_alpha()
    image = pygame.transform.scale(image, (48, 48))

    mask = pygame.mask.from_surface(image)


    transform = Transform(
        random.randint(40, WIDTH - 40),
        random.randint(40, HEIGHT - 40)
    )

    rect = image.get_rect(center=(transform.x, transform.y))

    return Ghost(
        image=image,
        transform=transform,
        rect=rect,
        mask=mask,
        speed=100
    )


def detect_collision(rect1: pygame.Rect, collectible: Collectible, sound: pygame.mixer.sound) -> bool:
    global score
    if rect1.colliderect(collectible.rect):
        score += collectible.orb.points
        sound.play()
        collectible.transform.x = random.randint(40, WIDTH - 40)
        collectible.transform.y = random.randint(40, HEIGHT - 40)
        collectible.rect.center = (collectible.transform.x, collectible.transform.y)

def draw_mask(
        screen: pygame.Surface,
        mask: pygame.mask.Mask,
        position: tuple[int, int],
) -> None:
    mask_surface = mask.to_surface(
        setcolor=(0, 150, 255, 120),
        unsetcolor=(0, 0, 0, 0),
    )
    screen.blit(mask_surface, position)

def main()->None:
    global score
    clock = pygame.time.Clock()

    moving = False
    facing_left = False

    player_idle_frames = load_animation_frames(
        "assets/Player16x16.png",
        16,
        16,
        3,
        row=3,
        frame_count=4,
    )

    player_run_frames = load_animation_frames(
        "assets/Player16x16.png",
        16,
        16,
        3,
        row=1,
        frame_count=4,
    )

    player_animation = Animation(
        frames=player_idle_frames,
        frame_index=0,
        timer=0,
        frame_duration=0.1,
    )

    player_transform = Transform(
        WIDTH // 2,
        HEIGHT // 2
    )

    player_image = player_animation.frames[player_animation.frame_index]
    player_rect = player_image.get_rect(center=(player_transform.x, player_transform.y))

    orbs = [
        create_orb("assets/orb_green.png", 10),
        create_orb("assets/orb_yellow.png", 20),
        create_orb("assets/orb_purple.png", 30),
        create_orb("assets/orb_red.png", 40),
    ]

    ghost = create_ghost()

    game_over = False

    coin_sound = pygame.mixer.Sound("assets/coin.wav")

    score = 0
    font = pygame.font.Font(None, 36)

    speed = 200

    running = True

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_rect.x -= speed * dt
            facing_left = True
            moving = True
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_rect.x += speed * dt
            facing_left = False
            moving = True
       
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_rect.y -= speed * dt
            moving = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_rect.y += speed * dt
            moving = True

        if not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            moving = False
            
        player_rect.clamp_ip(screen.get_rect())

        if moving:
            player_animation.frames = player_run_frames
        else:
            player_animation.frames = player_idle_frames

        player_image = player_animation.frames[player_animation.frame_index]

        if facing_left:
            player_image = pygame.transform.flip(player_image, True, False)

        player_mask = pygame.mask.from_surface(player_image)

        player_animation.timer += dt

        if player_animation.timer >= player_animation.frame_duration:
            player_animation.timer = 0
            player_animation.frame_index += 1

            if player_animation.frame_index >= len(player_animation.frames):
                player_animation.frame_index = 0

        if not game_over:
            if ghost.rect.x < player_rect.x:
                ghost.rect.x += ghost.speed * dt
            if ghost.rect.x > player_rect.x:
                ghost.rect.x -= ghost.speed * dt
            if ghost.rect.y < player_rect.y:
                ghost.rect.y += ghost.speed * dt
            if ghost.rect.y > player_rect.y:
                ghost.rect.y -= ghost.speed * dt
            
            offset = (
                ghost.rect.x - player_rect.x,
                ghost.rect.y - player_rect.y,
            )

            if player_mask.overlap(ghost.mask, offset):
                game_over = True

        
        for orb in orbs:
            detect_collision(player_rect, orb, coin_sound)
        
        screen.fill((15, 15, 25))

        for orb in orbs:
            screen.blit(orb.image, orb.rect)

        screen.blit(ghost.image, ghost.rect)
        screen.blit(player_image, player_rect)

        pygame.draw.rect(screen, (255, 0, 0), player_rect, 2)
        pygame.draw.rect(screen, (0, 255, 0), ghost.rect, 2)

        draw_mask(screen, player_mask, player_rect.topleft)
        draw_mask(screen, ghost.mask, ghost.rect.topleft)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        if game_over:
            moving = False
            game_over_text = font.render("GAME OVER - Press R", True, (255, 255, 255))
            screen.blit(game_over_text, (250, 280))

        if game_over and keys[pygame.K_r]:
            score = 0
            player_rect.center = (WIDTH // 2, HEIGHT // 2)
            ghost.rect.center = (random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40))
            game_over = False
            

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()