# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    import datetime
    startTime = datetime.datetime.now()
    max_nodes_expanded = 1

    # Implementing fringe list as stack in case of dfs.
    fringe_list = util.Stack()
    path_explored = {}          # For storing path by keeping track of parent nodes
    visited = {}

    startState = problem.getStartState()
    goalState = ()

    # Adding start in the path_explored
    path_explored[startState] = [(startState, " ")]
    fringe_list.push(startState)
    # variable to keep track of the size of the fringelist
    count = 1
    import sys


    while not fringe_list.isEmpty():
        top = fringe_list.pop()
        count -= 1

        if problem.isGoalState(top):
            # Goal state reached
            goalState = top
            break

        successors = problem.getSuccessors(top)
        if top not in visited:
            # mark the top as visited
            visited[top] = True

        # Pushing all unvisited successors to fringe list
        for successor in successors:
            if successor[0] not in visited:
                fringe_list.push(successor[0])
                count += 1
                if count>max_nodes_expanded:
                    max_nodes_expanded = count
                # add successors in the fringe list and add them in the path with top as their parent.
                path_explored[successor[0]] = [(top, successor[1])]

    # Calculating the path directions based on the path_explored dictionary.
    path_directions = []
    x = path_explored[goalState]
    while (x[0][0] is not startState):
        path_directions.insert(0, x[0][1])
        x = path_explored[x[0][0]]

    # adding the start state at the first place in path_directions list.
    path_directions.insert(0, x[0][1])

    # Converting and returning the path_directions in the form required.
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    path_directions = list(map(lambda b: b.replace("West", w), path_directions))
    path_directions = list(map(lambda b: b.replace("East", e), path_directions))
    path_directions = list(map(lambda b: b.replace("North", n), path_directions))
    path_directions = list(map(lambda b: b.replace("South", s), path_directions))

    endTime = datetime.datetime.now()
    timeTaken = endTime - startTime

    print "\nTime taken for depth first search: ", timeTaken.microseconds / 1000, " milliseconds"
    print "\nMax_nodes_expanded: ",max_nodes_expanded
    print "\nHence, Memory consumed by fringe_list (in bytes): ",max_nodes_expanded*sys.getsizeof(startState)

    return path_directions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    import datetime
    startTime = datetime.datetime.now()
    max_nodes_expanded = 1
    startState = problem.getStartState()
    # Implementing fringe list as queue in case of bfs.
    fringe_list = util.Queue()
    visited = []

    fringe_list.push((startState,[]))
    visited.append(startState)

    count = 1
    import sys

    while not fringe_list.isEmpty():
        # Pop front of the queue. Hence the nodes are expanded in fcfs fashion.
        front,directions = fringe_list.pop()
        count -= 1

        if problem.isGoalState(front):
            break

        successors = problem.getSuccessors(front)

        # Pushing all unvisited successors to fringe list
        for s in successors:
            if s[0] not in visited:
                fringe_list.push((s[0],directions + [s[1]]))
                count = count + 1
                if count > max_nodes_expanded:
                    max_nodes_expanded = count
                visited.append(s[0])

    # snippet for recording execution time of the algorithm.
    endTime = datetime.datetime.now()
    timeTaken = endTime - startTime

    print "\nTime taken for breadth first search: ", timeTaken.microseconds / 1000, " milliseconds"
    print "\nMax_nodes_expanded: ", max_nodes_expanded
    print "Hence, Memory consumed by fringe_list (in bytes): ", max_nodes_expanded * sys.getsizeof(startState),"\n"
    return directions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    import datetime
    import sys
    startTime = datetime.datetime.now()
    max_nodes_expanded = 1

    # Implementing fringe list as priority queue in case of ucs.
    fringe_list = util.PriorityQueue()
    visited = []

    startState = problem.getStartState()
    # Adding a list along with start state to keep track of the directions the pacman takes.
    fringe_list.push((startState, []), 0)
    count = 1

    while not fringe_list.isEmpty():
        front, directions = fringe_list.pop()
        count -= 1

        if problem.isGoalState(front):
            break

        if front not in visited:
            successors = problem.getSuccessors(front)

            # Pushing all unvisited successors to fringe list
            for s in successors:
                if s[0] not in visited:
                    # adding the current action to the list of directions. These directions are again stored in the
                    # state of the successor.
                    actions = directions + [s[1]]
                    fringe_list.push((s[0],actions),problem.getCostOfActions(actions))
                    count += 1
                    if count > max_nodes_expanded:
                        max_nodes_expanded = count
            visited.append(front)

    endTime = datetime.datetime.now()
    timeTaken = endTime - startTime

    print "\nTime taken for uniform cost search: ", timeTaken.microseconds / 1000, " milliseconds"
    print "\nMax_nodes_expanded: ", max_nodes_expanded
    print "\nHence, Memory consumed by fringe_list (in bytes): ", max_nodes_expanded * sys.getsizeof(startState)
    return directions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    import datetime
    import sys
    startTime = datetime.datetime.now()
    max_nodes_expanded = 1

    # Implementing fringe list as priority queue in case of A* search.
    fringe_list = util.PriorityQueue()
    visited = []

    startState = problem.getStartState()
    # In case of A* search, the cost of a node consists of the actual distance till the node + the estimate (heuristic)
    # cost from that node to goal state i.e. g(n)+h(n).
    fringe_list.push((startState, []), heuristic(startState, problem))
    count =1
    while not fringe_list.isEmpty():
        top, directions = fringe_list.pop()
        count = count - 1
        # Goal state reached
        if problem.isGoalState(top):
            break

        if top not in visited:
            successors = problem.getSuccessors(top)

            # Pushing all unvisited successors to fringe list
            for successor in successors:
                if successor[0] not in visited:
                    actions = directions + [successor[1]]
                    # Similar to the start state, adding heuristic cost to the total cost of the successors.
                    fringe_list.push((successor[0],actions), problem.getCostOfActions(actions) + heuristic(successor[0], problem))
                    count += 1
                    if count > max_nodes_expanded:
                        max_nodes_expanded = count
            visited.append(top)

    endTime = datetime.datetime.now()
    timeTaken = endTime - startTime

    print "\nTime taken for A* search: ", timeTaken.microseconds / 1000, " milliseconds"
    print "\nMax_nodes_expanded: ", max_nodes_expanded
    print "Hence, Memory consumed by fringe_list (in bytes): ", max_nodes_expanded * sys.getsizeof(startState), "\n"
    return directions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
