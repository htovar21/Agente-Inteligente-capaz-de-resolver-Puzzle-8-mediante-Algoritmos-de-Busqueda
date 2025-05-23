import random
from collections import deque

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
    if row > 0: moves.append((-3, "Up"))    # arriba
    if row < 2: moves.append((3, "Down"))   # abajo
    if col > 0: moves.append((-1, "Left"))  # izquierda
    if col < 2: moves.append((1, "Right"))  # derecha

    for move, move_name in moves:
        new_pos = zero_pos + move
        new_state = list(state)
        new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
        neighbors.append((tuple(new_state), move_name))
    return neighbors

def bfs(start, goal):
    if start == goal:
        return [(start, None)]

    queue = deque([start])
    visited = set([start])
    parent = {start: (None, None)}  # estado: (padre, movimiento)

    while queue:
        current = queue.popleft()
        for neighbor, move_name in get_neighbors_with_moves(current):
            if neighbor not in visited:
                parent[neighbor] = (current, move_name)
                if neighbor == goal:
                    path = []
                    state = neighbor
                    while state is not None:
                        p, m = parent[state]
                        path.append((state, m))
                        state = p
                    path.reverse()
                    return path
                visited.add(neighbor)
                queue.append(neighbor)
    return None

initial_state = generate_solvable_initial(goal_state)

print("🧩 Estado inicial aleatorio resoluble:")
for i in range(3):
    print(initial_state[i*3:(i+1)*3])
print("\n🎯 Estado objetivo:")
for i in range(3):
    print(goal_state[i*3:(i+1)*3])

solution = bfs(initial_state, goal_state)

if solution:
    print(f"\n✅ Solución encontrada en {len(solution)-1} pasos:")
    for i, (state, move) in enumerate(solution):
        if i == 0:
            print(f"\nPaso {i} (Inicio):")
        else:
            print(f"\nPaso {i}: Movimiento {move}")
        for j in range(3):
            print(state[j*3:(j+1)*3])
else:
    print("\n❌ No se encontró solución.")
