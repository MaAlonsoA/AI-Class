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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack

    class Root:
        def __init__(self, position: tuple, path: list):
            self.position = position
            self.path = path

        def getPosition(self):
            return self.position

        def getPath(self):
            return self.path

    visited: set = set()
    rootsStack: Stack = Stack()

    initialRoot: Root = Root(problem.getStartState(), [])
    rootsStack.push(initialRoot)

    while not rootsStack.isEmpty():

        currentNode = rootsStack.pop()

        if problem.isGoalState(currentNode.getPosition()):
            return currentNode.getPath()
        else:
            visited.add(currentNode.getPosition())
            successors = problem.getSuccessors(currentNode.getPosition())
            for nextNode in successors:
                nextNodePosition: tuple = nextNode[0]
                if nextNodePosition not in visited:
                    nextMove: str = nextNode[1]

                    newPath = currentNode.getPath().copy()
                    newPath.append(nextMove)
                    nextNode: Root = Root(nextNodePosition, newPath)

                    rootsStack.push(nextNode)
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    class Root:
        def __init__(self, position: tuple, path: list) -> None:
            self.position = position
            self.path = path

        def getPosition(self) -> tuple:
            return self.position

        def getPath(self) -> list:
            return self.path

    visited: set = set()
    rootsQueue: Queue = Queue()
    rootsQueue.push(Root(problem.getStartState(), []))  # Push initial root

    while not rootsQueue.isEmpty():

        currentNode: Root = rootsQueue.pop()

        if problem.isGoalState(currentNode.getPosition()):
            return currentNode.getPath()
        else:
            visited.add(currentNode.getPosition())
            successors = problem.getSuccessors(currentNode.getPosition())
            for nextNode in successors:
                nextNodePosition: tuple = nextNode[0]
                if nextNodePosition not in visited:
                    visited.add(nextNodePosition)

                    nextMove: str = nextNode[1]

                    newPath: list = currentNode.getPath().copy()
                    newPath.append(nextMove)
                    nextNode: Root = Root(nextNodePosition, newPath)

                    rootsQueue.push(nextNode)
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    class Root:
        def __init__(self, position: tuple, path: list, cost: int) -> None:
            self.position = position
            self.path = path
            self.cost = cost

        def getPosition(self) -> tuple:
            return self.position

        def getPath(self) -> list:
            return self.path

        def getCost(self) -> int:
            return self.cost

    visited: set = set()
    rootsQueue: PriorityQueue = PriorityQueue()
    # Push initial root with priority 0
    rootsQueue.push(Root(problem.getStartState(), [], 0), 0)

    while not rootsQueue.isEmpty():

        currentNode: Root = rootsQueue.pop()

        if currentNode.getPosition() not in visited:
            visited.add(currentNode.getPosition())
            if problem.isGoalState(currentNode.getPosition()):
                return currentNode.getPath()
            else:
                successor: list = problem.getSuccessors(
                    currentNode.getPosition())
                for nextNode in successor:
                    nextNodePosition = nextNode[0]
                    if nextNodePosition not in visited:
                        nextMove = nextNode[1]
                        newPath: list = currentNode.getPath().copy()
                        newPath.append(nextMove)
                        nextCost = nextNode[2]
                        newCost = currentNode.getCost() + nextCost
                        rootsQueue.push(
                            Root(nextNodePosition, newPath, newCost), newCost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    class Root:
        def __init__(self, position: tuple, path: list, cost: int) -> None:
            self.position = position
            self.path = path
            self.cost = cost

        def getPosition(self) -> tuple:
            return self.position

        def getPath(self) -> list:
            return self.path

        def getCost(self) -> int:
            return self.cost

    visited: set = set()
    rootsQueue: PriorityQueue = PriorityQueue()

    rootsQueue.push(Root(problem.getStartState(), [], 0),
                    0)  # Push the initial root

    while not rootsQueue.isEmpty():
        currentNode: Root = rootsQueue.pop()

        if problem.isGoalState(currentNode.getPosition()):
            return currentNode.getPath().copy()

        if currentNode.getPosition() not in visited:
            visited.add(currentNode.getPosition())
            successors: list = problem.getSuccessors(currentNode.getPosition())
            for nextNode in successors:
                nextNodePostition: tuple = nextNode[0]
                if nextNodePostition not in visited:
                    nextMove: str = nextNode[1]
                    newPath: list = currentNode.getPath().copy()
                    newPath.append(nextMove)
                    newCost: int = problem.getCostOfActions(
                        newPath) + heuristic(nextNodePostition, problem)
                    if nextNodePostition not in visited:
                        rootsQueue.push(
                            Root(nextNodePostition, newPath, newCost), newCost)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
