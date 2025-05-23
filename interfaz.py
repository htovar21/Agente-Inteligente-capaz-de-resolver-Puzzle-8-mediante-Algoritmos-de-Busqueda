import pygame
import sys
from BFS import goal_state, generate_solvable_initial, bfs
from Astar_Manhattan import astar
import time
from tabulate import tabulate  # <-- Importar tabulate

pygame.init()
pygame.font.init()

# --- Configuración PyGame ---
SIZE = WIDTH, HEIGHT = 300, 450
TILE_SIZE = 90
FPS = 5

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Puzzle 8")

font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 30)

BG_COLOR = (30, 30, 30)
TILE_COLOR = (70, 130, 180)
EMPTY_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

btn_change = pygame.Rect(30, 370, 100, 50)
btn_start = pygame.Rect(170, 370, 100, 50)
btn_restart = pygame.Rect(30, 370, 100, 50)
btn_astar = pygame.Rect(170, 370, 100, 50)

def print_comparison_table(bfs_stats, astar_stats):
    headers = ["Algoritmo", "Nodos Expandidos", "Longitud Solución", "Tiempo (s)"]
    data = [
        ["BFS", bfs_stats[0], bfs_stats[1], f"{bfs_stats[2]:.4f}"],
        ["A*", astar_stats[0], astar_stats[1], f"{astar_stats[2]:.4f}"],
    ]
    table = tabulate(data, headers, tablefmt="fancy_grid", numalign="right")
    print("\n" + table + "\n")

def draw_state(state):
    screen.fill(BG_COLOR)
    for i, val in enumerate(state):
        row, col = divmod(i, 3)
        x = col * TILE_SIZE + 15
        y = row * TILE_SIZE + 50
        rect = pygame.Rect(x, y, TILE_SIZE - 10, TILE_SIZE - 10)

        if val == 0:
            pygame.draw.rect(screen, EMPTY_COLOR, rect)
        else:
            pygame.draw.rect(screen, TILE_COLOR, rect)
            text = font.render(str(val), True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def draw_text(text, y):
    rendered = small_font.render(text, True, TEXT_COLOR)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    text_surf = small_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_comparison(bfs_stats, astar_stats):
    # Recibe tuplas: (nodes_expanded, solution_length, time_elapsed)
    y_start = 150
    line_height = 30
    texts = [
        "Comparación de algoritmos:",
        f"BFS: Nodos expandidos = {bfs_stats[0]}, Longitud = {bfs_stats[1]}, Tiempo = {bfs_stats[2]:.4f} s",
        f"A*: Nodos expandidos = {astar_stats[0]}, Longitud = {astar_stats[1]}, Tiempo = {astar_stats[2]:.4f} s",
    ]
    for i, text in enumerate(texts):
        draw_text(text, y_start + i * line_height)

def main():
    clock = pygame.time.Clock()
    initial_state = None
    solution = []
    step_idx = 0
    mode = "menu"
    algorithm = "BFS"

    astar_executed = False
    bfs_stats = None  # (nodes_expanded, solution_length, time_elapsed)
    astar_stats = None
    comparing = False  # modo comparación

    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == "menu":
                    if btn_change.collidepoint(event.pos):
                        initial_state = generate_solvable_initial(goal_state)
                        astar_executed = False
                        comparing = False
                        bfs_stats = None
                        astar_stats = None
                    elif btn_start.collidepoint(event.pos):
                        if not initial_state:
                            initial_state = generate_solvable_initial(goal_state)
                        solution, nodes_exp, sol_len, time_elapsed = bfs(initial_state, goal_state)
                        bfs_stats = (nodes_exp, sol_len, time_elapsed)
                        algorithm = "BFS"
                        if solution:
                            print(f"[BFS] Solución encontrada en {sol_len} pasos.")
                            mode = "solving"
                            step_idx = 0
                            comparing = False
                        else:
                            print("[BFS] No se encontró solución.")
                elif mode == "finished":
                    if btn_restart.collidepoint(event.pos):
                        initial_state = None
                        solution = []
                        step_idx = 0
                        mode = "menu"
                        astar_executed = False
                        comparing = False
                        bfs_stats = None
                        astar_stats = None
                    elif btn_astar.collidepoint(event.pos):
                        if not astar_executed:
                            if initial_state:
                                result = astar(initial_state, goal_state)
                                if result:
                                    solution, nodes_exp, sol_len, time_elapsed = result
                                    astar_stats = (nodes_exp, sol_len, time_elapsed)
                                    algorithm = "A*"
                                    print(f"[A*] Solución encontrada en {sol_len} pasos.")
                                    mode = "solving"
                                    step_idx = 0
                                    astar_executed = True
                                    comparing = False
                                else:
                                    print("[A*] No se encontró solución.")
                            else:
                                print("⚠️ Debes ejecutar BFS primero para establecer el estado inicial.")
                        else:
                            # Aquí activamos modo comparar y mostramos estadísticas en consola
                            if bfs_stats and astar_stats:
                                comparing = True
                                print_comparison_table(bfs_stats, astar_stats)
                            else:
                                print("⚠️ Ejecuta BFS y A* primero para comparar.")

        # DIBUJADO
        if mode == "menu":
            if not initial_state:
                initial_state = generate_solvable_initial(goal_state)
            draw_state(initial_state)
            draw_text("Busqueda No Informada BFS", 20)
            draw_text("Estado inicial", HEIGHT - 115)
            draw_button(btn_change, "Cambiar", mouse_pos)
            draw_button(btn_start, "Comenzar", mouse_pos)
            comparing = False

        elif mode == "solving":
            if step_idx < len(solution):
                state, move = solution[step_idx]
                draw_state(state)
                draw_text(f"Búsqueda {'No Informada BFS' if algorithm == 'BFS' else 'Informada A*'}", 20)
                if move:
                    draw_text(f"Movimiento: {move}", HEIGHT - 50)
                else:
                    draw_text("Estado inicial", HEIGHT - 50)
                step_idx += 1
            else:
                mode = "finished"

        elif mode == "finished":
            draw_state(solution[-1][0])
            draw_text(f"Búsqueda {'No Informada BFS' if algorithm == 'BFS' else 'Informada A*'}", 20)
            draw_text(f"Estado Meta - {len(solution) - 1} pasos", HEIGHT - 115)
            draw_button(btn_restart, "Reiniciar", mouse_pos)

            if astar_executed and not comparing:
                draw_button(btn_astar, "Comparar", mouse_pos)
            elif not astar_executed:
                draw_button(btn_astar, "A*", mouse_pos)

            if comparing:
                draw_comparison(bfs_stats, astar_stats)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
