############################################################
# Section 2: Grid Navigation
############################################################

    # Returns a set of possible moves from the current position in the given
    # scene as a set of points
def successors(node, scene):
    x = node[0]
    y = node[1]
    r = len(scene)
    c = None
    if r != 0:
        c = len(scene[0])
    if x + 1 < r and scene[x + 1][y] == False:
        yield (x + 1, y)
    if x - 1 >= 0 and x - 1 < r and scene[x - 1][y] == False:
        yield (x - 1, y)
    if y + 1 < c and scene[x][y + 1] == False:
        yield (x, y + 1)
    if y - 1 >= 0 and y - 1 < c and scene[x][y - 1] == False:
        yield (x, y - 1)
    if x + 1 < r and y + 1 < c and scene[x + 1][y + 1] == False:
        yield (x + 1, y + 1)
    if x - 1 >= 0 and x - 1 < r and y - 1 >= 0 and y - 1 < c and scene[x - 1][y - 1] == False:
        yield (x - 1, y - 1)
    if x + 1 < r and y - 1 >= 0 and y - 1 < c and scene[x + 1][y - 1] == False:
        yield (x + 1, y - 1)
    if x - 1 >= 0 and x - 1 < r and y + 1 < c and scene[x - 1][y + 1] == False:
        yield (x - 1, y + 1)

# Get the heuristic eucliedean distance between the current state and the
# goal state
def eucliedean_distance(current, goal):
    x1 = current[0]
    y1 = current[1]
    x2 = goal[0]
    y2 = goal[1]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Use A* Search to navigate through obstacles


def find_path(start, goal, scene):
    # to do: take care of goal on obstacle or no solution
    queue = Queue.PriorityQueue()
    explored_set = set()
    parent = {}
    parent[start] = start
    moves = {}
    moves[start] = start
    queue.put((eucliedean_distance(start, goal), 0, start))
    explored_set.add(start)
    solution = []
    while not queue.empty():
        current = queue.get()
        current_position = current[2]
        distance_so_far = current[1]
        for successor in successors(current_position, scene):
            if successor not in explored_set:
                parent[successor] = current_position
                if successor == goal:
                    # backtrack through the solution to get the moves
                    node = successor
                    while(parent[node] != node):
                        solution.append(node)
                        node = parent[node]
                    solution.append(node)
                    return list(reversed(solution))
                # add the node to the queue with it's scores and mark it as
                # explored
                x = eucliedean_distance(current_position, successor)
                queue.put(
                    (eucliedean_distance(successor, goal) + distance_so_far + x, distance_so_far + x, successor))
                explored_set.add(successor)
    return None
