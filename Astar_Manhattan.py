import heapq  # Importa heapq para manejar la cola de prioridad eficiente
import time   # Importa time para medir tiempo de ejecución

# Estado objetivo del puzzle 8 (tablero 3x3)
goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)  # El 0 representa el espacio vacío

def manhattan_distance(state):
    """
    Calcula la suma de las distancias Manhattan de cada ficha a su posición objetivo.
    La distancia Manhattan es la suma de las diferencias absolutas en filas y columnas.
    """
    distance = 0
    for i, val in enumerate(state):
        if val == 0:  # Ignorar el espacio vacío
            continue
        # Encontrar la posición objetivo de la ficha val
        goal_index = goal_state.index(val)
        # Coordenadas actuales (fila, columna)
        x1, y1 = divmod(i, 3)
        # Coordenadas objetivo (fila, columna)
        x2, y2 = divmod(goal_index, 3)
        # Sumar la distancia Manhattan para esta ficha
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_neighbors(state):
    """
    Genera los estados vecinos del estado actual moviendo el espacio vacío.
    Devuelve una lista de tuplas (nuevo_estado, movimiento_realizado).
    """
    neighbors = []
    zero_index = state.index(0)         # Encuentra la posición del espacio vacío (0)
    x, y = divmod(zero_index, 3)        # Convierte la posición lineal a coordenadas fila, columna
    # Movimientos posibles: arriba, abajo, izquierda, derecha
    moves = {
        'Arriba': (-1, 0),
        'Abajo': (1, 0),
        'Izquierda': (0, -1),
        'Derecha': (0, 1)
    }

    for move, (dx, dy) in moves.items():
        nx, ny = x + dx, y + dy  # Nueva posición después del movimiento
        # Verifica que la nueva posición esté dentro del tablero 3x3
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_index = nx * 3 + ny  # Calcula el índice lineal de la nueva posición
            new_state = list(state)  # Convierte la tupla a lista para poder modificarla

            # Intercambia el espacio vacío con la ficha en la nueva posición
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append(((tuple(new_state), move)))  # Añade el nuevo estado y movimiento a la lista
    return neighbors

def astar(initial_state, goal_state):
    """
    Implementa el algoritmo A* para encontrar el camino óptimo desde initial_state a goal_state.
    """
    start_time = time.time()  # Marca el tiempo de inicio
    frontier = []  # Cola de prioridad para estados por explorar
    
    # Inserta el estado inicial con prioridad f = g + h (0 + heurística)
    heapq.heappush(frontier, (0 + manhattan_distance(initial_state), 0, initial_state, []))
    explored = set()  # Conjunto para estados ya visitados
    nodes_expanded = 0  # Contador de nodos expandidos

    while frontier:
        # Extrae el estado con menor prioridad f
        f, cost, state, path = heapq.heappop(frontier)
        nodes_expanded += 1

        # Si el estado actual es el objetivo, termina y reconstruye el camino
        if state == goal_state:
            end_time = time.time()  # Tiempo de finalización

            solution_path = path + [(state, None)]  # Ruta completa con el estado final

            solution_length = len(solution_path) - 1  # Número de movimientos
            
            time_elapsed = end_time - start_time  # Tiempo total transcurrido
            return solution_path, nodes_expanded, solution_length, time_elapsed

        explored.add(state)  # Marca el estado actual como visitado

        # Explora todos los vecinos del estado actual
        for neighbor, move in get_neighbors(state):
            if neighbor in explored:
                continue  # Ignora vecinos ya visitados

            new_cost = cost + 1  # Incrementa el costo g (un movimiento más)
            new_path = path + [(state, move)]  # Actualiza el camino recorrido
            priority = new_cost + manhattan_distance(neighbor)  # Calcula f = g + h
            # Añade el vecino a la cola de prioridad para ser explorado
            heapq.heappush(frontier, (priority, new_cost, neighbor, new_path))

    end_time = time.time()  # Fin del algoritmo si no encuentra solución
    return None, nodes_expanded, 0, end_time - start_time
