import pygame
import sys
from BFS import goal_state, generate_solvable_initial, bfs

pygame.init()
pygame.font.init()

# --- Configuración PyGame ---

SIZE = WIDTH, HEIGHT = 300, 350
TILE_SIZE = 90
FPS = 1

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Puzzle 8 - BFS con PyGame")

font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 30)

BG_COLOR = (30, 30, 30)
TILE_COLOR = (70, 130, 180)
EMPTY_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

def draw_state(state):
    screen.fill(BG_COLOR)
    for i, val in enumerate(state):
        row, col = divmod(i, 3)
        x = col * TILE_SIZE + 15
        y = row * TILE_SIZE + 15
        rect = pygame.Rect(x, y, TILE_SIZE - 10, TILE_SIZE -10)

        if val == 0:
            pygame.draw.rect(screen, EMPTY_COLOR, rect)
        else:
            pygame.draw.rect(screen, TILE_COLOR, rect)
            text = font.render(str(val), True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def draw_text(text, y):
    rendered = small_font.render(text, True, TEXT_COLOR)
    rect = rendered.get_rect(center=(WIDTH//2, y))
    screen.blit(rendered, rect)

def main():
    initial_state = generate_solvable_initial(goal_state)
    solution = bfs(initial_state, goal_state)

    if not solution:
        print("No se encontró solución para este estado inicial.")
        pygame.quit()
        sys.exit()

    print(f"Solución encontrada en {len(solution)-1} pasos.")

    clock = pygame.time.Clock()
    step_idx = 0

    running = True
    try:
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            state, move = solution[step_idx]

            draw_state(state)
            if move:
                draw_text(f"Movimiento: {move}", HEIGHT - 30)
            else:
                draw_text("Estado inicial", HEIGHT - 30)

            pygame.display.flip()

            if step_idx < len(solution) - 1:
                step_idx += 1
            else:
                pygame.time.wait(2000)
                running = False
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
