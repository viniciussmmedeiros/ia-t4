import random
import math
from typing import Tuple, Callable




def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    depth = 0
    v, a = MAX(state, -math.inf, math.inf, eval_func, max_depth, depth)
    
    return a


def MAX(s, alpha, beta, eval_func, max_depth, depth):
    if s.is_terminal() or (depth >= max_depth and max_depth != -1): 
        return eval_func(s, s.player), None
    depth += 1
    v = alpha
    a = (0,0)
    SUCESSORES = []
    for move in s.legal_moves():
        SUCESSORES.append((s.next_state(move), move))

    for s1, a1 in SUCESSORES:
        v1, x =  MIN(s1,alpha,beta,eval_func,max_depth, depth)
        if (v1 > v): 
            v = v1
            a = a1	#atualiza v e a
        alpha= max(alpha, v)		#atualiza 𝛼 
        if (alpha >= beta): 
            break #sai do loop: o MIN que chamou tem uma alternativa β melhor que 𝛼.
    
    return v, a

def MIN(s, alpha, beta, eval_func, max_depth, depth):
    if s.is_terminal() or (depth >= max_depth and max_depth != -1): 
         return -eval_func(s, s.player), None
    depth += 1
    v = beta
    a = (0,0)
    SUCESSORES = []

    for move in s.legal_moves():
        SUCESSORES.append((s.next_state(move), move))

    for s1, a1 in SUCESSORES:
        v1, x =  MAX(s1,alpha,beta,eval_func, max_depth, depth)
        if (v1 < v): 
            v = v1
            a = a1	#atualiza v e a
        beta = min(beta, v)	#atualiza 𝛼 
        if (beta <= alpha): 
            break #sai do loop: o MIN que chamou tem uma alternativa β melhor que 𝛼.

    return v, a
