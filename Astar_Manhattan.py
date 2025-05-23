import heapq

goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)

def manhattan_distance(state):
    distance = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        goal_index = goal_state.index(val)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_index, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

def get_neighbors(state):
    neighbors = []
    zero_index = state.index(0)
    x, y = divmod(zero_index, 3)
    moves = {
        'Arriba': (-1, 0),
        'Abajo': (1, 0),
        'Izquierda': (0, -1),
        'Derecha': (0, 1)
    }

    for move, (dx, dy) in moves.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_index = nx * 3 + ny
            new_state = list(state)
            new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
            neighbors.append(((tuple(new_state), move)))
    return neighbors

def astar(initial_state, goal_state):
    frontier = []
    heapq.heappush(frontier, (0 + manhattan_distance(initial_state), 0, initial_state, []))
    explored = set()

    while frontier:
        f, cost, state, path = heapq.heappop(frontier)
        if state == goal_state:
            return path + [(state, None)]
        explored.add(state)

        for neighbor, move in get_neighbors(state):
            if neighbor in explored:
                continue
            new_cost = cost + 1
            new_path = path + [(state, move)]
            priority = new_cost + manhattan_distance(neighbor)
            heapq.heappush(frontier, (priority, new_cost, neighbor, new_path))

    return None  # No solución