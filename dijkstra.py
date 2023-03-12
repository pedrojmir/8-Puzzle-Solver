import time, heapq

heapQStructure = []
visited = {}

goal_state =      [1,2,3,
                  4,5,6,
                  7,8,0]

initial_puzzle = [1,2,4,
                  6,7,3,
                  8,5,0]

# Check if initial puzzle is solvable by counting the number of inversions in the initial state and the goal state
# If the number of inversions is odd, the puzzle is not solvable
def is_solvable(initial_state, goal_state):
    # Get the number of inversions in the initial state
    inversions = 0
    for i in range(len(initial_state)):
        for j in range(i + 1, len(initial_state)):
            if initial_state[i] != 0 and initial_state[j] != 0 and initial_state[i] > initial_state[j]:
                inversions += 1
    # Get the number of inversions in the goal state
    for i in range(len(goal_state)):
        for j in range(i + 1, len(goal_state)):
            if goal_state[i] != 0 and goal_state[j] != 0 and goal_state[i] > goal_state[j]:
                inversions += 1
    # If the number of inversions is odd, the puzzle is not solvable
    return inversions % 2 == 0

def dijkstra(initial_state, goal_state):
    # Check if the initial state is solvable
    if not is_solvable(initial_state, goal_state):
        return None

    # Create the first state with cost to reach, initial board_state, & path.
    first_state = [0,initial_state, []]
    heapq.heappush(heapQStructure, (first_state[0], first_state)) # Push (total_cost,[total_cost,initial_state, ["start"]]) 
    
    # Loop until the heapQStructure is empty, if found return the path and amount of moves.
    while heapQStructure:
        # Pop the top state from the heapQStructure
        state = heapq.heappop(heapQStructure)
        tempStateAsString = ''.join(str(i) for i in state[1][1])
        # Check if the state has been visited with a lower cost
        if(tempStateAsString in visited):
            # Ignore the state if it has been visited with a lower cost
            if(state[0] > visited[tempStateAsString]):    
                continue
        check_state = state[1][1]
        # Check if the state is the goal state
        if check_state == goal_state:
            final_path = state[1][2]
            return state[0], final_path # The -1 is to remove the "start" from the path
        # Add the state to the explored set
        stateAsString = ''.join(str(i) for i in state[1][1])
        visited[stateAsString] = state[0]
        # Generate the successors of the state
        neighbors = find_neighbors(state[1], visited, state[0])
        # Loop through the successors in reverse order 
        for successor in neighbors[::-1]:
            # Check if the successor has not been explored 
            stateAsStringTemp = ''.join(str(i) for i in successor[1][1])
            # Push on to stack if not visited, else check if cost is less than the one in visited
            if stateAsStringTemp not in visited:
                
                # Add the successor to the heapQStructure with the path to reach it
                visited[stateAsStringTemp] = successor[0]
                heapq.heappush(heapQStructure,successor)
            else:
                # Check if cost is less than the one in visited
                if successor[0] < visited[stateAsStringTemp]:
                    # Update cost and path
                    heapq.heappush(heapQStructure,successor)
                    visited[stateAsStringTemp] = successor[0]
    # If the goal state is not found, return None
    return None

# try every possible move and return the list of neighbors
def find_neighbors(state, visited, total_cost):
    # Get the indexLocation of the 0 value to know what tile is empty
    indexLocation = state[1].index(0)
    # Get the row and column of the blank tile
    row = indexLocation // 3 # 6//3 = 2
    col = indexLocation % 3 # 6%3 = 0
    # Initialize the list of neighbors
    neighbors = []
    # Check if the zero tile is not in the first row
    # If zero is not on the top row, also know as row 0
    if row != 0:
        # Move the tile down
        new_state = state[1][:]
        # number_tile, zero_tile = zero_tile, number_tile, add cost of moved number_tile
        new_state[indexLocation], new_state[indexLocation - 3] = new_state[indexLocation - 3], new_state[indexLocation]
        new_total_cost = new_state[indexLocation] + total_cost
        neighbors.append((new_total_cost, [new_total_cost, new_state, state[2] + ["down"]]))
    if row != 2:
        # Move the tile up
        new_state = state[1][:]
        new_state[indexLocation], new_state[indexLocation + 3] = new_state[indexLocation + 3], new_state[indexLocation]
        new_total_cost = new_state[indexLocation] + total_cost
        neighbors.append((new_total_cost, [new_total_cost, new_state, state[2] + ["updown"]]))
    if col != 0:
        # Move the tile right
        new_state = state[1][:]
        new_state[indexLocation], new_state[indexLocation - 1] = new_state[indexLocation - 1], new_state[indexLocation]
        new_total_cost = new_state[indexLocation] + total_cost
        neighbors.append((new_total_cost, [new_total_cost, new_state, state[2] + ["right"]]))
    if col != 2:
        # Move the tile left
        new_state = state[1][:]
        new_state[indexLocation], new_state[indexLocation + 1] = new_state[indexLocation + 1], new_state[indexLocation]
        new_total_cost = new_state[indexLocation] + total_cost
        neighbors.append((new_total_cost, [new_total_cost, new_state, state[2] + ["left"]]))
    return neighbors


start_time = time.time()

try:
    cost, path = dijkstra(initial_puzzle, goal_state)
    print("The path is", path, "\nThe weighted-cost is " + str(cost) + ".\nThe time is to execute was", round((time.time() - start_time), 6), "seconds.")
except:
    print("Not solvable")
