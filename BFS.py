import random
from collections import deque
import time

# Estado objetivo que queremos alcanzar en el puzzle 8 (0 representa el espacio vacío)
goal_state = (1, 2, 3,
              8, 0, 4,
              7, 6, 5)

def count_inversions(state):
    """
    Cuenta el número de inversiones en el estado.
    Una inversión es cuando un número mayor aparece antes que uno menor.
    El 0 (espacio vacío) se excluye.
    """
    nums = [n for n in state if n != 0]
    inv_count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inv_count += 1
    return inv_count

def generate_random_initial(goal):
    """
    Genera un estado inicial aleatorio diferente al estado objetivo.
    """
    while True:
        initial = tuple(random.sample(range(9), 9))  # Permutación aleatoria de números 0-8
        if initial != goal:
            return initial

def get_neighbors_with_moves(state):
    """
    Obtiene los estados vecinos que se pueden alcanzar moviendo
    el espacio vacío (0) en las direcciones posibles:
    arriba, abajo, izquierda y derecha.
    Devuelve una lista de tuplas (nuevo_estado, nombre_del_movimiento).
    """
    neighbors = []
    zero_pos = state.index(0)  # Posición actual del espacio vacío
    row, col = divmod(zero_pos, 3)  # Coordenadas fila y columna en la matriz 3x3

    moves = []
    # Comprobamos las posibles direcciones de movimiento según la posición del 0
    if row > 0: moves.append((-3, "Arriba"))    # Mover espacio vacío hacia arriba (fila anterior)
    if row < 2: moves.append((3, "Abajo"))      # Mover espacio vacío hacia abajo (fila siguiente)
    if col > 0: moves.append((-1, "Izquierda")) # Mover espacio vacío hacia la izquierda (columna anterior)
    if col < 2: moves.append((1, "Derecha"))    # Mover espacio vacío hacia la derecha (columna siguiente)

    for move, move_name in moves:
        new_pos = zero_pos + move
        new_state = list(state)
        # Intercambiar el espacio vacío con la pieza adyacente correspondiente
        new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
        neighbors.append((tuple(new_state), move_name))
    return neighbors

def bfs(start, goal):
    """
    Implementa la búsqueda en anchura (BFS) para encontrar la secuencia de movimientos
    que transforma el estado inicial en el estado objetivo.

    Retorna:
    - path: lista de tuplas (estado, movimiento que se hizo para llegar a ese estado)
    - nodes_expanded: cantidad de nodos expandidos durante la búsqueda
    - solution_length: longitud de la solución (cantidad de movimientos)
    - time_elapsed: tiempo que tardó la búsqueda en segundos
    """
    if start == goal:
        # Caso trivial donde el estado inicial ya es el objetivo
        return [(start, None)], 0, 0, 0.0

    start_time = time.time()
    queue = deque([start])  # Cola para BFS
    visited = set([start])  # Conjunto para evitar estados repetidos
    parent = {start: (None, None)}  # Diccionario que guarda para cada estado su padre y movimiento
    nodes_expanded = 0

    while queue:
        current = queue.popleft()  # Extraemos el estado del frente de la cola
        nodes_expanded += 1
        for neighbor, move_name in get_neighbors_with_moves(current):
            if neighbor not in visited:
                parent[neighbor] = (current, move_name)  # Guardamos padre y movimiento para reconstruir el camino
                if neighbor == goal:
                    # Si llegamos al objetivo, reconstruimos el camino desde el objetivo al inicio
                    end_time = time.time()
                    path = []
                    state = neighbor
                    while state is not None:
                        p, m = parent[state]
                        path.append((state, m))
                        state = p
                    path.reverse()  # Invertimos para tener camino desde el inicio al objetivo
                    solution_length = len(path) - 1  # Cantidad de movimientos
                    time_elapsed = end_time - start_time
                    return path, nodes_expanded, solution_length, time_elapsed
                visited.add(neighbor)
                queue.append(neighbor)

    end_time = time.time()
    # No se encontró solución
    return None, nodes_expanded, 0, end_time - start_time
