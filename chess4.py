import chess
import random
import sys
import time

# board = chess.Board('r1b1kb1r/pppp1ppp/5q2/4n3/3KP3/2N3PN/PPP4P/R1BQ1B1R b kq - 0 1')
board = chess.Board()
simulated_depth = 1
max_eval = None
best_move = None
best_score = float('-inf')
nodes_searched = 0

def evaluate(state, move):

    try:
        if getattr(state.outcome(), 'winner') == None:
            eval_result = 0
        elif getattr(state.outcome(), 'winner') == True:
            eval_result = float('-inf')
        elif getattr(state.outcome(), 'winner') == False:
            eval_result = float('inf')
    except:
        # print(chess.BaseBoard.piece_map(state))

        w_pawns = str(chess.BaseBoard.pieces(state, 1, True)).count('1')
        w_knights = str(chess.BaseBoard.pieces(state, 2, True)).count('1')
        w_bishops = str(chess.BaseBoard.pieces(state, 3, True)).count('1')
        w_rooks = str(chess.BaseBoard.pieces(state, 4, True)).count('1')
        w_queens = str(chess.BaseBoard.pieces(state, 5, True)).count('1')

        b_pawns = str(chess.BaseBoard.pieces(state, 1, False)).count('1')
        b_knights = str(chess.BaseBoard.pieces(state, 2, False)).count('1')
        b_bishops = str(chess.BaseBoard.pieces(state, 3, False)).count('1')
        b_rooks = str(chess.BaseBoard.pieces(state, 4, False)).count('1')
        b_queens = str(chess.BaseBoard.pieces(state, 5, False)).count('1')

        white_score = w_pawns + w_knights*3 + w_bishops*3 + w_rooks*4 + w_queens*9
        black_score = b_pawns + b_knights*3 + b_bishops*3 + b_rooks*4 + b_queens*9
        # print('White Score:', white_score, '\nBlack Score:', black_score, '\n')

        eval_result = black_score - white_score
    
    return eval_result

def select_best_move(eval_result):
    best_moves_list = []

    for key, value in eval_result.items():
        if max(eval_result.values()) == value:
            best_moves_list.append(key)

    move = random.choice(best_moves_list)

    return move

def evaluate_next_move(state):
    legal_moves_list = list(board.legal_moves)
    legal_moves_result_dict = {}
    for move in legal_moves_list:
        state.push(move)
        legal_moves_result_dict[move] = evaluate(state, move)
        # print(chess.BaseBoard.unicode(board))
        state.pop()

    for key, value in legal_moves_result_dict.items():
        print(key, ' : ', value)
    # print(legal_moves_result_dict)

    return legal_moves_result_dict

def minimax(state, depth, maximizing_player):
    global simulated_depth, max_eval, best_move, best_score, nodes_searched

    nodes_searched += 1
    # print(nodes_searched)

    # print(depth, state.move_stack, evaluate(state, None))
    if depth == simulated_depth or state.is_game_over() == True:
        evaluated_state = evaluate(state, None)
        # print(depth, state.move_stack, evaluated_state)

        if evaluated_state >= best_score:
            best_score = evaluated_state
            best_move = state.move_stack[len(state.move_stack)-depth]

        return evaluated_state

    if maximizing_player == True:
        max_eval = float('-inf')
        for available_move in list(board.legal_moves):
            state.push(available_move)
            eval = minimax(state, depth+1, False)
            max_eval = max(max_eval, eval)
            state.pop()

        return max_eval


    elif maximizing_player == False:
        min_eval = float('inf')
        for available_move in list(board.legal_moves):
            state.push(available_move)
            eval = minimax(state, depth+1, True)
            min_eval = min(min_eval, eval)
            state.pop()
        
        return min_eval

def check_eval_result_reason(state):
    if state.is_checkmate() == True:
        eval_result_reason = 'Checkmate'
    elif state.is_stalemate() == True:
        eval_result_reason = 'Stalemate'
    elif state.is_fivefold_repetition() == True:
        eval_result_reason = 'Fivefold repetition'
    elif state.is_insufficient_material() == True:
        eval_result_reason = 'Insufficient material'
    elif state.is_seventyfive_moves() == True:
        eval_result_reason = '75 moves'
    else:
        eval_result_reason = None

    return eval_result_reason

cont = True

while cont == True:
    print(chess.BaseBoard.unicode(board))
    print()

    if board.is_game_over() != False:
        cont = False
        print('Reason:', check_eval_result_reason(board))
  
    if cont == True:

        if board.turn == False:
            start_time = time.time()
            nodes_searched = 0
            move = minimax(board, 0, True)
            move = best_move
            end_time = time.time()

            print()
            print(nodes_searched, 'nodes')
            print(round(end_time-start_time, 2), 'seconds')
            print(round(nodes_searched/(end_time-start_time),2), 'nodes/second')

            # legal_moves_list = list(board.legal_moves)
            # move = random.choice(legal_moves_list)

            print('\nCPU selected move:', move)
            # print(board.peek())
            board.push(move)
            # print('State:', board.push(move))

        elif board.turn == True:
            valid_move = False
            while valid_move == False:
                legal_moves_list = list(board.legal_moves)
                input_move = input('Enter your move: ')
                try:
                    uci_move = chess.Move.from_uci(input_move)
                except:
                    if input_move == 'exit' or 'Exit':
                        sys.exit()
                    uci_move = 0000
                if uci_move in legal_moves_list:
                    board.push(uci_move)
                    print()
                    valid_move = True
                else:
                    print('This is an invalid move. Please try again.\n')
        else:
            print('Error')

print('Outcome:', board.outcome())