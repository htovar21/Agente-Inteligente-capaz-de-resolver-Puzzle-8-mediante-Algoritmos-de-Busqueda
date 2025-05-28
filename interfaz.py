import pygame
import sys
from BFS import goal_state, generate_random_initial, bfs
from Astar_Manhattan import astar
import time
from tabulate import tabulate

pygame.init()
pygame.font.init()

# Configuración ventana y constantes
TAMANO = ANCHO, ALTO = 300, 450
TAM_CASILLA = 90
FPS = 5

pantalla = pygame.display.set_mode(TAMANO)
pygame.display.set_caption("Puzzle 8")

# Fuentes para textos grandes y pequeños
fuente_grande = pygame.font.SysFont(None, 72)
fuente_pequena = pygame.font.SysFont(None, 30)

# Colores usados en la interfaz
COLOR_FONDO = (30, 30, 30)
COLOR_CASILLA = (70, 130, 180)
COLOR_VACIO = (50, 50, 50)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (100, 100, 100)
COLOR_BOTON_HOVER = (150, 150, 150)

# Rectángulos para botones (posición y tamaño)
boton_cambiar = pygame.Rect(30, 370, 100, 50)
boton_comenzar = pygame.Rect(170, 370, 100, 50)
boton_reiniciar = pygame.Rect(30, 370, 100, 50)
boton_astar = pygame.Rect(170, 370, 100, 50)

def imprimir_tabla_comparativa(estad_bfs, estad_astar):
    # Muestra por consola una tabla comparativa con resultados de BFS y A*
    encabezados = ["Algoritmo", "Nodos Expandidos", "Longitud Solución", "Tiempo (s)"]
    datos = [
        ["BFS", estad_bfs[0], estad_bfs[1], f"{estad_bfs[2]:.4f}"],
        ["A*", estad_astar[0], estad_astar[1], f"{estad_astar[2]:.4f}"],
    ]
    tabla = tabulate(datos, encabezados, tablefmt="fancy_grid", numalign="right")
    print("\n" + tabla + "\n")

def dibujar_estado(estado):
    # Dibuja el estado actual del puzzle en la pantalla
    pantalla.fill(COLOR_FONDO) # Limpia la pantalla con el color de fondo
    for i, val in enumerate(estado):
        fila, columna = divmod(i, 3)
        x = columna * TAM_CASILLA + 15
        y = fila * TAM_CASILLA + 50
        rect = pygame.Rect(x, y, TAM_CASILLA - 10, TAM_CASILLA - 10)

        if val == 0:
            pygame.draw.rect(pantalla, COLOR_VACIO, rect)  # Casilla vacía
        else:
            pygame.draw.rect(pantalla, COLOR_CASILLA, rect) # Casilla con número
            texto = fuente_grande.render(str(val), True, COLOR_TEXTO)
            rect_texto = texto.get_rect(center=rect.center)
            pantalla.blit(texto, rect_texto)

def dibujar_texto(texto, y):
    # Dibuja texto centrado horizontalmente en una posición y vertical dada
    renderizado = fuente_pequena.render(texto, True, COLOR_TEXTO)
    rect = renderizado.get_rect(center=(ANCHO // 2, y))
    pantalla.blit(renderizado, rect)

def dibujar_boton(rect, texto, pos_mouse):
    # Dibuja un botón con cambio de color si el mouse está encima
    color = COLOR_BOTON_HOVER if rect.collidepoint(pos_mouse) else COLOR_BOTON
    pygame.draw.rect(pantalla, color, rect)
    texto_surf = fuente_pequena.render(texto, True, COLOR_TEXTO)
    rect_texto = texto_surf.get_rect(center=rect.center)
    pantalla.blit(texto_surf, rect_texto)

def dibujar_comparacion(estad_bfs, estad_astar):
    # Dibuja en pantalla la comparación de estadísticas BFS vs A*
    ancho_tabla = 320
    alto_tabla = 120
    pos_x_tabla = 20
    pos_y_tabla = 120
    pygame.draw.rect(pantalla, (60, 60, 60), (pos_x_tabla, pos_y_tabla, ancho_tabla, alto_tabla), border_radius=10)

    y_inicial = pos_y_tabla + 10
    alto_linea = 30

    encabezado = ["", "Nodos", "  Long.", "   Tiempo"]
    fila_bfs = ["BFS", str(estad_bfs[0]), f"    {estad_bfs[1]}", f"    {estad_bfs[2]:.4f}"]
    fila_astar = ["A*", str(estad_astar[0]), f"    {estad_astar[1]}", f"    {estad_astar[2]:.4f}"]
    tabla = [encabezado, fila_bfs, fila_astar]

    for idx_fila, fila in enumerate(tabla):
        for idx_col, texto in enumerate(fila):
            x_pos = pos_x_tabla + 10 + idx_col * 60
            y_pos = y_inicial + idx_fila * alto_linea
            renderizado = fuente_pequena.render(texto, True, COLOR_TEXTO)
            pantalla.blit(renderizado, (x_pos, y_pos))

def handle_menu(eventos, pos_mouse, estado):
    # Dibuja el estado inicial y muestra los botones principales
    dibujar_estado(estado["initial_state"])
    dibujar_texto("Busqueda No Informada BFS", 20)
    dibujar_texto("Estado inicial", ALTO - 115)

    # Mostrar mensaje si no hay solución
    if estado["no_solution"]:
        dibujar_texto("No es resoluble", ALTO - 90, )

    dibujar_boton(boton_cambiar, "Cambiar", pos_mouse)
    dibujar_boton(boton_comenzar, "Comenzar", pos_mouse)
    estado["comparing"] = False

    # Manejo de eventos del menú
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_cambiar.collidepoint(evento.pos):
                # Genera un nuevo estado inicial aleatorio
                estado["initial_state"] = generate_random_initial(goal_state)
                estado["astar_executed"] = False
                estado["comparing"] = False
                estado["bfs_stats"] = None
                estado["astar_stats"] = None
                estado["no_solution"] = False
            elif boton_comenzar.collidepoint(evento.pos):
                # Ejecuta BFS desde el estado inicial
                solucion, nodos_exp, long_sol, tiempo = bfs(estado["initial_state"], goal_state)
                estado["bfs_stats"] = (nodos_exp, long_sol, tiempo)
                estado["algorithm"] = "BFS"
                if solucion:
                    print(f"[BFS] Solución encontrada en {long_sol} pasos.")
                    estado["solution"] = solucion
                    estado["step_idx"] = 0
                    estado["no_solution"] = False
                    return "solving"
                else:
                    print("No es resoluble")
                    estado["no_solution"] = True
    return "menu"

def handle_solving(eventos, pos_mouse, estado):
    # Muestra el progreso de la solución paso a paso
    if estado["step_idx"] < len(estado["solution"]):
        estado_actual, movimiento = estado["solution"][estado["step_idx"]]
        dibujar_estado(estado_actual)
        dibujar_texto(f"Búsqueda {'No Informada BFS' if estado['algorithm'] == 'BFS' else 'Informada A*'}", 20)
        if movimiento:
            dibujar_texto(f"Movimiento: {movimiento}", ALTO - 50)
        else:
            dibujar_texto("Estado inicial", ALTO - 50)
        estado["step_idx"] += 1
        return "solving"
    else:
        return "finished"

def handle_finished(eventos, pos_mouse, estado):
    # Pantalla final con opción para reiniciar o comparar BFS con A*
    dibujar_estado(estado["solution"][-1][0])
    dibujar_texto(f"Búsqueda {'No Informada BFS' if estado['algorithm'] == 'BFS' else 'Informada A*'}", 20)
    dibujar_texto(f"Estado Meta - {len(estado['solution']) - 1} pasos", ALTO - 115)
    dibujar_boton(boton_reiniciar, "Reiniciar", pos_mouse)

    if estado["astar_executed"] and not estado["comparing"]:
        dibujar_boton(boton_astar, "Comparar", pos_mouse)
    elif not estado["astar_executed"]:
        dibujar_boton(boton_astar, "A*", pos_mouse)

    if estado["comparing"]:
        dibujar_comparacion(estado["bfs_stats"], estado["astar_stats"])

    # Eventos en pantalla final
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_reiniciar.collidepoint(evento.pos):
                # Reinicia el juego y estados
                estado["initial_state"] = generate_random_initial(goal_state)
                estado["solution"] = []
                estado["step_idx"] = 0
                estado["astar_executed"] = False
                estado["comparing"] = False
                estado["bfs_stats"] = None
                estado["astar_stats"] = None
                return "menu"

            elif boton_astar.collidepoint(evento.pos):
                # Ejecuta A* o muestra comparación si ya fue ejecutado
                if not estado["astar_executed"]:
                    if estado["initial_state"]:
                        resultado = astar(estado["initial_state"], goal_state)
                        if resultado:
                            solucion, nodos_exp, long_sol, tiempo = resultado
                            estado["astar_stats"] = (nodos_exp, long_sol, tiempo)
                            estado["algorithm"] = "A*"
                            print(f"[A*] Solución encontrada en {long_sol} pasos.")
                            estado["solution"] = solucion
                            estado["step_idx"] = 0
                            estado["astar_executed"] = True
                            estado["comparing"] = False
                            return "solving"
                        else:
                            print("[A*] No se encontró solución.")
                    else:
                        # Si ya se ejecutó A*, mostrar comparación
                        print(" Debes ejecutar BFS primero para establecer el estado inicial.")
                else:
                    if estado["bfs_stats"] and estado["astar_stats"]:
                        estado["comparing"] = True
                        imprimir_tabla_comparativa(estado["bfs_stats"], estado["astar_stats"])
                    else:
                        print(" Ejecuta ambos algoritmos primero para comparar.")

    return "finished"

def main():
    reloj = pygame.time.Clock()
    estado = {
        "initial_state": generate_random_initial(goal_state),
        "solution": [],
        "step_idx": 0,
        "algorithm": None,
        "astar_executed": False,
        "comparing": False,
        "bfs_stats": None,
        "astar_stats": None,
        "no_solution": False,
    }

    estado_actual = "menu"

    while True:
        eventos = pygame.event.get()
        pos_mouse = pygame.mouse.get_pos()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if estado_actual == "menu":
            estado_actual = handle_menu(eventos, pos_mouse, estado)
        elif estado_actual == "solving":
            estado_actual = handle_solving(eventos, pos_mouse, estado)
        elif estado_actual == "finished":
            estado_actual = handle_finished(eventos, pos_mouse, estado)

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()
