# multiAgents.py
# --------------
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


from sys import maxsize
import sys
from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        import pacman
        import game
        import sys
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState: pacman.gameState = currentGameState.generatePacmanSuccessor(
            action)
        newPos = successorGameState.getPacmanPosition()
        newFood: game.Grid = successorGameState.getFood()
        newGhostStates: list = successorGameState.getGhostStates()

        "*** YOUR CODE HERE ***"
        if action == "Stop":
            return -sys.maxsize - 1

        result: int = 0
        goals: list = newFood.asList()
        if not goals:
            return sys.maxsize * 2 + 1

        distancesToGoals: list = list(
            manhattanDistance(goal, newPos) for goal in goals)
        distancesToGoals.sort(reverse=False)

        distancesToGhosts: list = list(manhattanDistance(
            ghost.getPosition(), newPos) for ghost in newGhostStates)
        distancesToGhosts.sort(reverse=False)

        result += 1/distancesToGoals[0] * distancesToGhosts[0]
        result += successorGameState.getScore()

        return result


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth: int):
            depth += 1
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            else:
                value: int = -sys.maxsize - 1
                legalActions: list = state.getLegalActions(0)
                for action in legalActions:
                    value = max(value, minValue(
                        state.generateSuccessor(0, action), 1, depth))
                return value

        def minValue(state, ghostIndex: int, depth: int):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            else:
                value: int = sys.maxsize * 2 + 1
                legalActions: list = state.getLegalActions(ghostIndex)
                if ghostIndex == state.getNumAgents() - 1:
                    for action in legalActions:
                        value = min(value, maxValue(
                            state.generateSuccessor(ghostIndex, action), depth))
                else:
                    for action in legalActions:
                        value = min(value, minValue(state.generateSuccessor(
                            ghostIndex, action), ghostIndex + 1, depth))
            return value

        pacManMoves: list = gameState.getLegalActions(0)
        value: int = -sys.maxsize - 1
        move: str = Directions.STOP
        for currentMove in pacManMoves:
            currentValue = minValue(
                gameState.generateSuccessor(0, currentMove), 1, 0)
            if (currentValue > value):
                value = currentValue
                move = currentMove
        return move


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth: int, alpha: int, beta: int):
            depth += 1
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            value: int = -sys.maxsize - 1
            legalActions: list = state.getLegalActions(0)
            for action in legalActions:
                value = max(value, minValue(
                    state.generateSuccessor(0, action), 1, depth, alpha, beta))
                if beta < value:
                    return value
                alpha = max(alpha, value)
            return value

        def minValue(state, ghostIndex: int, depth: int, alpha: int, beta: int):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            value: int = sys.maxsize * 2 + 1
            legalActions: list = state.getLegalActions(ghostIndex)
            for action in legalActions:
                if ghostIndex == state.getNumAgents() - 1:
                    value = min(value, maxValue(
                        state.generateSuccessor(ghostIndex, action), depth, alpha, beta))
                    if alpha > value:
                        return value
                    beta = min(beta, value)
                else:
                    for action in legalActions:
                        value = min(value, minValue(state.generateSuccessor(
                            ghostIndex, action), ghostIndex + 1, depth, alpha, beta))
                        if alpha > value:
                            return value
                        beta = min(beta, value)
            return value

        value: int = -sys.maxsize - 1
        alpha: int = -sys.maxsize - 1
        beta: int = sys.maxsize*2+1
        move: str = 'Directions.STOP'
        pacManMoves: list = gameState.getLegalActions(0)
        for currentMove in pacManMoves:
            currentValue = minValue(
                gameState.generateSuccessor(0, currentMove), 1, 0, alpha, beta)
            if currentValue > value:
                value = currentValue
                move = currentMove
            if currentValue > beta:
                return move
            alpha = max(alpha, value)
        return move


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth: int):
            depth += 1

            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            
            value: int = -sys.maxsize - 1
            legalActions: list = state.getLegalActions(0)
            for action in legalActions:
                value = max(value, expectValue(
                    state.generateSuccessor(0, action), 1, depth))

            return value

        def expectValue(state, ghostIndex: int, depth: int):

            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            legalActions: list = state.getLegalActions(ghostIndex)
            expectation: int = 0

            if len(legalActions) == 0:
                return 0
            for action in legalActions:
                if ghostIndex == state.getNumAgents() - 1:
                    value = maxValue(state.generateSuccessor(
                        ghostIndex, action), depth)
                else:
                    value = expectValue(state.generateSuccessor(
                        ghostIndex, action), ghostIndex + 1, depth)
                expectation += value / len(legalActions)

            return expectation

        pacManMoves: list = gameState.getLegalActions(0)
        value: int = -sys.maxsize - 1
        move: str = Directions.STOP
        for currentMove in pacManMoves:
            currentValue = expectValue(
                gameState.generateSuccessor(0, currentMove), 1, 0)
            if currentValue > value:
                value = currentValue
                move = currentMove

        return move


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
