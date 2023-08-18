import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
import math

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    Consider that this will be called in the Othello tournament situation,
    so you should call the best implementation you got.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque a sua implementacao da poda alpha-beta

    if state.game_name == 'Othello':
    #     return random.choice([(2, 3), (4, 5), (5, 4), (3, 2)])

        NUM_ITERATIONS = 100
        root_node = MCTSNode(state)
        for _ in range(NUM_ITERATIONS):
            node = select(root_node)
            result = simulate(node.state)
            backpropagate(node, result, state.player)
        
        best_child = None
        most_visits = -1

        for child in root_node.children:
            if child.visits > most_visits:
                best_child = child
                most_visits = child.visits

        return best_child.move

class MCTSNode:
    def __init__(self, state, parent = None, move = None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.move = move

def select(node):
    while not node.state.is_terminal() and (len(node.children) == len(node.state.legal_moves())):
        selected_child = None
        best_value = float('-inf')
        for child in node.children:
            ucb_value = ucb(child)
            if ucb_value > best_value:
                best_value = ucb_value
                selected_child = child
        node = selected_child

    if not node.state.is_terminal():
        legal_moves = list(node.state.legal_moves())
        unexplored_moves = [move for move in legal_moves 
                                    if move not in 
                                        [child.move for child in node.children]]

        if unexplored_moves:
            move = random.choice(unexplored_moves)
            new_state = node.state.next_state(move)
            new_node = MCTSNode(new_state, parent = node, move = move)
            node.children.append(new_node)
            node = new_node

    return node

def simulate(state):
    while not state.is_terminal():
        move = random.choice(list(state.legal_moves()))
        state = state.next_state(move)

    return state.winner()

def ucb(node):
    C = 1

    exploitation = node.value / node.visits
    exploration = C * math.sqrt(2 * math.log(node.parent.visits) / node.visits)
    return exploitation + exploration

def backpropagate(node, result, player):
    while node != None:
        node.visits += 1
        if result == player:
            node.value += 1
        node = node.parent