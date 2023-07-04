import math
import random
import time

import pygame

pygame.init()

WIDTH: int = 800
HEIGHT: int = 600
TOP_BAR_HEIGHT: int = 50
LABEL_FONT: pygame.font.Font = pygame.font.SysFont("comicsans", 24)

win: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT: int = 400
TARGET_EVENT: int = pygame.USEREVENT

TARGET_PADDING: int = 30

BG_COLOR: tuple[int, int, int] = (0, 25, 40)

LIVES: int = 3


class Target:
    MAX_SIZE: int = 30
    GROWTH_RATE: float = 0.2
    COLOR: str = "red"
    SECOND_COLOR: str = "white"

    def __init__(self, x: int, y: int, size: float = 0.0):
        self.x: int = x
        self.y: int = y
        self.size: float = size
        self.grow: bool = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x: int, y: int) -> bool:
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2) <= self.size


def format_time(secs: float) -> str:
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


def draw_top_bar(
    win: pygame.Surface, elapsed_time: float, targets_pressed: int, misses: int
) -> None:
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))

    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


def draw(win: pygame.Surface, targets: list[Target]) -> None:
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


def get_middle(surface: pygame.Surface) -> float:
    return WIDTH / 2 - surface.get_width() / 2


def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: %{accuracy}", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.KEYDOWN
            ):
                quit()


def main() -> None:
    run: bool = True
    targets: list[Target] = []
    clock: pygame.time.Clock = pygame.time.Clock()

    targets_pressed: int = 0
    clicks: int = 0
    misses: int = 0
    start_time: float = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)

        click: bool = False

        elapsed_time: float = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                targets.append(
                    Target(
                        random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING),
                        random.randint(
                            TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING
                        ),
                    )
                )

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*pygame.mouse.get_pos()):
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_screen(win, elapsed_time, targets_pressed, clicks)

        draw(win, targets)
        draw_top_bar(win, elapsed_time, targets_pressed, misses)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
