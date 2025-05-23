import random
from collections import deque
import time

goal_state = (1, 2, 3,
              8, 0, 4,
              7, 6, 5)

def count_inversions(state):
    nums = [n for n in state if n != 0]
    inv_count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                inv_count += 1
    return inv_count

def is_solvable(start, goal):
    return count_inversions(start) % 2 == count_inversions(goal) % 2

def generate_solvable_initial(goal):
    while True:
        initial = tuple(random.sample(range(9), 9))
        if is_solvable(initial, goal) and initial != goal:
            return initial

def get_neighbors_with_moves(state):
    neighbors = []
    zero_pos = state.index(0)
    row, col = divmod(zero_pos, 3)

    moves = []
    if row > 0: moves.append((-3, "Arriba"))    # arriba
    if row < 2: moves.append((3, "Abajo"))      # abajo
    if col > 0: moves.append((-1, "Izquierda")) # izquierda
    if col < 2: moves.append((1, "Derecha"))    # derecha

    for move, move_name in moves:
        new_pos = zero_pos + move
        new_state = list(state)
        new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
        neighbors.append((tuple(new_state), move_name))
    return neighbors

def bfs(start, goal):
    if start == goal:
        return [(start, None)], 0, 0, 0.0  # path, nodes_expanded, solution_length, time_elapsed

    start_time = time.time()
    queue = deque([start])
    visited = set([start])
    parent = {start: (None, None)}  # estado: (padre, movimiento)
    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1
        for neighbor, move_name in get_neighbors_with_moves(current):
            if neighbor not in visited:
                parent[neighbor] = (current, move_name)
                if neighbor == goal:
                    end_time = time.time()
                    path = []
                    state = neighbor
                    while state is not None:
                        p, m = parent[state]
                        path.append((state, m))
                        state = p
                    path.reverse()
                    solution_length = len(path) - 1
                    time_elapsed = end_time - start_time
                    return path, nodes_expanded, solution_length, time_elapsed
                visited.add(neighbor)
                queue.append(neighbor)

    end_time = time.time()
    # Si no encuentra solución, retorna None con métricas 0
    return None, nodes_expanded, 0, end_time - start_time
