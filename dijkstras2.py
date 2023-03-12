import time
import heapq

initial_puzzle = [1,2,5,
                  4,6,3,
                  7,8,0]
goal_state = [1,2,3,
              4,5,6,
              7,8,0]

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

# initial_puzzle = [1,2,3,
#                   4,5,0,
#                   7,8,6]
# goal_state =     [1,2,3,
#                   4,5,6,
#                   7,8,0]
start_time = time.time()


def dfs(initial_state, goal_state):
    if not is_solvable(initial_state, goal_state):
        print("Not solvable")
        return None
    #(0, [initial_state, ["start"]])?
    first_state = [0,initial_state, ["start"]]
    heapQStructure = []
    heapq.heappush(first_state[0], first_state) # push [0,initial_state, ["start"]] 
    print("Yo ")
    print(heapQStructure)
    visited = []
    
    # Loop until the heapQStructure is empty, if found return the path and amount of moves.
    while heapQStructure:
        # Pop the top state from the heapQStructure
        state = heapQStructure.pop()
        check_state = state[0]
        # Check if the state is the goal state
        if check_state == goal_state:
            final_path = state[1]
            return (len(final_path)-1), final_path # The -1 is to remove the "start" from the path
        
        # Add the state to the explored set
        visited.append(state[0])
        # Generate the successors of the state
        neighbors = find_neighbors(state, visited)
        # Loop through the successors in reverse order 
        for successor in neighbors[::-1]:
            # Check if the successor has not been explored 
            if successor[0] not in visited:
                # Add the successor to the heapQStructure with the path to reach it
                heapQStructure.append(successor)
    # If the goal state is not found, return None
    print("Not found end state.")
    return None




def find_neighbors(state, visited):
    # Get the indexLocation of the 0 value to know what tile is empty

    indexLocation = state[0].index(0)
    # Get the row and column of the blank tile
    row = indexLocation // 3
    col = indexLocation % 3
    # Initialize the list of neighbors
    neighbors = []
    # Check if the zero tile is not in the first row
    if row != 0:
        # Move the tile up
        new_state = state[0][:]
        new_state[indexLocation], new_state[indexLocation - 3] = new_state[indexLocation - 3], new_state[indexLocation]
        # Add the new state to the list of neighbors
        if new_state not in visited:
            new_path = state[1] + ["up"]
            if new_state == goal_state:
                print("Found goal state")
                return [(new_state, new_path)] 
            neighbors.append((new_state, new_path))
    # Check if the zero tile is not in the last row
    if row != 2:
        # Move the tile down
        new_state = state[0][:]
        new_state[indexLocation], new_state[indexLocation + 3] = new_state[indexLocation + 3], new_state[indexLocation]
        # Add the new state to the list of neighbors
        if new_state not in visited:
            if new_state == goal_state:
                print("Found goal state")
                return [(new_state, new_path)]
            new_path = state[1] + ["down"]
            neighbors.append((new_state, new_path))
    # Check if the zero tile is not in the first column
    if col != 0:
        # Move the tile to the left
        new_state = state[0][:]
        new_state[indexLocation], new_state[indexLocation - 1] = new_state[indexLocation - 1], new_state[indexLocation]
        # Add the new state to the list of neighbors
        if new_state not in visited:
            if new_state == goal_state:
                print("Found goal state")
                return [(new_state, new_path)]
            new_path = state[1] + ["left"]
            neighbors.append((new_state, new_path))
    # Check if the zero tile is not in the last column
    if col != 2:
        # Move the tile to the right
        new_state = state[0][:]
        new_state[indexLocation], new_state[indexLocation + 1] = new_state[indexLocation + 1], new_state[indexLocation]
        # Add the new state to the list of successors
        if new_state not in visited:
            if new_state == goal_state:
                print("Found goal state")
                return [(new_state, new_path)]
            new_path = state[1] + ["right"]
            neighbors.append((new_state, new_path))
    return neighbors






cost, path = dfs(initial_puzzle, goal_state)
end_time = time.time()

print("The path is", path, "and the cost is", cost, "and the time is to execute was", round((time.time() - start_time),2), "seconds")

# More comments.