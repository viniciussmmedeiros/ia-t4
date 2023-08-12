import random
import math
from typing import Tuple

def make_move(state) -> Tuple[int, int]:
    NUM_ITERATIONS = 500
    root_node = MCTSNode(state)
    
    for _ in range(NUM_ITERATIONS):
        node = select(root_node)
        result = simulate(node.state)
        backpropagate(node, result)
    
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
    while not node.state.is_terminal():
        if not node.children:
            node = expand(node)
        elif all(child.visits > 0 for child in node.children):
            selected_child = None
            best_value = float('-inf')
            for child in node.children:
                ucb_value = ucb(child)
                if ucb_value > best_value:
                    best_value = ucb_value
                    selected_child = child
            node = selected_child
        else:
            unvisited_children = [child 
                                    for child in node.children 
                                        if child.visits == 0]
            return random.choice(unvisited_children)

    return node

def expand(node):
    legal_moves = list(node.state.legal_moves())

    if legal_moves:
        move = random.choice(legal_moves)
        new_state = node.state.next_state(move)
        new_node = MCTSNode(new_state, parent = node, move = move)
        node.children.append(new_node)

        return new_node

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

def backpropagate(node, winner):
    while node != None:
        node.visits += 1
        if winner == node.state.player:
            node.value += 1
        node = node.parent