import pygame
import sys
from BFS import goal_state, generate_solvable_initial, bfs
from Astar_Manhattan import astar
import time
from tabulate import tabulate

# Inicialización de Pygame y su módulo de fuentes
pygame.init()
pygame.font.init()

# Configuración de tamaño de ventana y otros parámetros
SIZE = WIDTH, HEIGHT = 300, 450
TILE_SIZE = 90
FPS = 5  # Frames por segundo para controlar la velocidad del juego

# Configuración de pantalla y título de la ventana
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Puzzle 8")

# Fuentes para los textos grandes y pequeños
font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 30)

# Colores usados en la interfaz
BG_COLOR = (30, 30, 30)
TILE_COLOR = (70, 130, 180)
EMPTY_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)

# Rectángulos que definen la posición y tamaño de botones en pantalla
btn_change = pygame.Rect(30, 370, 100, 50)
btn_start = pygame.Rect(170, 370, 100, 50)
btn_restart = pygame.Rect(30, 370, 100, 50)
btn_astar = pygame.Rect(170, 370, 100, 50)

# Función para imprimir tabla comparativa en consola entre BFS y A*
def print_comparison_table(bfs_stats, astar_stats):
    headers = ["Algoritmo", "Nodos Expandidos", "Longitud Solución", "Tiempo (s)"]
    data = [
        ["BFS", bfs_stats[0], bfs_stats[1], f"{bfs_stats[2]:.4f}"],
        ["A*", astar_stats[0], astar_stats[1], f"{astar_stats[2]:.4f}"],
    ]
    # Usa tabulate para crear una tabla con formato agradable
    table = tabulate(data, headers, tablefmt="fancy_grid", numalign="right")
    print("\n" + table + "\n")

# Función para dibujar el estado actual del puzzle en la pantalla
def draw_state(state):
    screen.fill(BG_COLOR)  # Fondo negro
    for i, val in enumerate(state):
        row, col = divmod(i, 3)  # Determinar fila y columna en la grilla 3x3
        x = col * TILE_SIZE + 15
        y = row * TILE_SIZE + 50
        rect = pygame.Rect(x, y, TILE_SIZE - 10, TILE_SIZE - 10)

        if val == 0:  # Casilla vacía
            pygame.draw.rect(screen, EMPTY_COLOR, rect)
        else:  # Casilla con número
            pygame.draw.rect(screen, TILE_COLOR, rect)
            text = font.render(str(val), True, TEXT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

# Dibuja texto centrado en la posición y dada
def draw_text(text, y):
    rendered = small_font.render(text, True, TEXT_COLOR)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    screen.blit(rendered, rect)

# Dibuja un botón, cambia color si el mouse está encima
def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    text_surf = small_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Dibuja una pequeña tabla comparativa de estadísticas dentro de la ventana
def draw_comparison(bfs_stats, astar_stats):
    table_width = 320
    table_height = 120
    table_x = 20
    table_y = 120
    pygame.draw.rect(screen, (60, 60, 60), (table_x, table_y, table_width, table_height), border_radius=10)

    y_start = table_y + 10
    line_height = 30

    # Cabecera y filas con datos
    header = ["", "Nodos", "  Long.", "   Tiempo"]
    bfs_row = ["BFS", str(bfs_stats[0]), f"    {bfs_stats[1]}", f"    {bfs_stats[2]:.4f}"]
    astar_row = ["A*", str(astar_stats[0]), f"    {astar_stats[1]}", f"    {astar_stats[2]:.4f}"]
    table = [header, bfs_row, astar_row]

    # Recorremos cada fila y columna para dibujar el texto
    for row_index, row in enumerate(table):
        for col_index, text in enumerate(row):
            x_pos = table_x + 10 + col_index * 60
            y_pos = y_start + row_index * line_height
            rendered = small_font.render(text, True, TEXT_COLOR)
            screen.blit(rendered, (x_pos, y_pos))

# --- Funciones para manejar estados del juego ---

# Estado del menú inicial donde se muestra estado inicial y botones Cambiar y Comenzar
def handle_menu(events, mouse_pos, state):
    draw_state(state["initial_state"])
    draw_text("Busqueda No Informada BFS", 20)
    draw_text("Estado inicial", HEIGHT - 115)
    draw_button(btn_change, "Cambiar", mouse_pos)
    draw_button(btn_start, "Comenzar", mouse_pos)
    state["comparing"] = False  # Desactivar modo comparación

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Cambiar estado inicial a uno nuevo resolvible
            if btn_change.collidepoint(event.pos):
                state["initial_state"] = generate_solvable_initial(goal_state)
                state["astar_executed"] = False
                state["comparing"] = False
                state["bfs_stats"] = None
                state["astar_stats"] = None
            # Ejecutar BFS para resolver
            elif btn_start.collidepoint(event.pos):
                solution, nodes_exp, sol_len, time_elapsed = bfs(state["initial_state"], goal_state)
                state["bfs_stats"] = (nodes_exp, sol_len, time_elapsed)
                state["algorithm"] = "BFS"
                if solution:
                    print(f"[BFS] Solución encontrada en {sol_len} pasos.")
                    state["solution"] = solution
                    state["step_idx"] = 0
                    return "solving"
                else:
                    print("[BFS] No se encontró solución.")

    return "menu"  # Mantener en menú

# Estado donde se muestra la solución paso a paso
def handle_solving(events, mouse_pos, state):
    if state["step_idx"] < len(state["solution"]):
        current_state, move = state["solution"][state["step_idx"]]
        draw_state(current_state)
        draw_text(f"Búsqueda {'No Informada BFS' if state['algorithm'] == 'BFS' else 'Informada A*'}", 20)
        if move:
            draw_text(f"Movimiento: {move}", HEIGHT - 50)
        else:
            draw_text("Estado inicial", HEIGHT - 50)
        state["step_idx"] += 1  # Avanza al siguiente paso
        return "solving"
    else:
        return "finished"  # Finalizó la solución

# Estado final, muestra el resultado y permite reiniciar o comparar BFS y A*
def handle_finished(events, mouse_pos, state):
    draw_state(state["solution"][-1][0])
    draw_text(f"Búsqueda {'No Informada BFS' if state['algorithm'] == 'BFS' else 'Informada A*'}", 20)
    draw_text(f"Estado Meta - {len(state['solution']) - 1} pasos", HEIGHT - 115)
    draw_button(btn_restart, "Reiniciar", mouse_pos)

    # Mostrar botón A* o Comparar según el estado
    if state["astar_executed"] and not state["comparing"]:
        draw_button(btn_astar, "Comparar", mouse_pos)
    elif not state["astar_executed"]:
        draw_button(btn_astar, "A*", mouse_pos)

    # Si está en modo comparación, mostrar tabla
    if state["comparing"]:
        draw_comparison(state["bfs_stats"], state["astar_stats"])

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Reiniciar el juego
            if btn_restart.collidepoint(event.pos):
                state["initial_state"] = generate_solvable_initial(goal_state)
                state["solution"] = []
                state["step_idx"] = 0
                state["astar_executed"] = False
                state["comparing"] = False
                state["bfs_stats"] = None
                state["astar_stats"] = None
                return "menu"

            # Ejecutar A* o alternar comparación
            elif btn_astar.collidepoint(event.pos):
                if not state["astar_executed"]:
                    if state["initial_state"]:
                        result = astar(state["initial_state"], goal_state)
                        if result:
                            solution, nodes_exp, sol_len, time_elapsed = result
                            state["astar_stats"] = (nodes_exp, sol_len, time_elapsed)
                            state["algorithm"] = "A*"
                            print(f"[A*] Solución encontrada en {sol_len} pasos.")
                            state["solution"] = solution
                            state["step_idx"] = 0
                            state["astar_executed"] = True
                            state["comparing"] = False
                            return "solving"
                        else:
                            print("[A*] No se encontró solución.")
                    else:
                        print("⚠️ Debes ejecutar BFS primero para establecer el estado inicial.")
                else:
                    if state["bfs_stats"] and state["astar_stats"]:
                        state["comparing"] = True
                        print_comparison_table(state["bfs_stats"], state["astar_stats"])
                    else:
                        print("⚠️ Ejecuta BFS y A* primero para comparar.")

    return "finished"

# Función principal donde corre el loop del juego
def main():
    clock = pygame.time.Clock()

    # Estado global del juego
    state = {
        "initial_state": generate_solvable_initial(goal_state),  # Estado inicial generable
        "solution": [],            # Lista de estados solución para mostrar
        "step_idx": 0,             # Índice del paso actual en la solución
        "mode": "menu",            # Modo actual (menu, solving, finished)
        "algorithm": "BFS",        # Algoritmo en ejecución
        "astar_executed": False,   # Flag si se ejecutó A*
        "bfs_stats": None,         # Estadísticas BFS
        "astar_stats": None,       # Estadísticas A*
        "comparing": False,        # Flag si está mostrando comparación
    }

    # Diccionario que mapea modos con funciones manejadoras
    mode_handlers = {
        "menu": handle_menu,
        "solving": handle_solving,
        "finished": handle_finished,
    }

    running = True
    while running:
        clock.tick(FPS)  # Controlar FPS
        mouse_pos = pygame.mouse.get_pos()
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:  # Salir si se cierra ventana
                running = False

        # Llama la función que corresponde al modo actual, actualizando el modo
        state["mode"] = mode_handlers[state["mode"]](events, mouse_pos, state)

        pygame.display.flip()  # Actualiza la pantalla

    pygame.quit()


if __name__ == "__main__":
    main()
