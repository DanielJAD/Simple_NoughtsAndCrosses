import random as rd
import numpy as np

board = [' - - - - - - - - ',
         '| a1   a2   a3 |',
         '| b1   b2   b3 |',
         '| c1   c2   c3 |',
         ' - - - - - - - - ']
index_it = np.array(list(range(0, 9)))

index_ax = np.array([
    ['a1', 'a2', 'a3'],
    ['b1', 'b2', 'b3'],
    ['c1', 'c2', 'c3']])


def fill_board(marks):
    return [' - - - - - - - - ',
            '|  ' + marks[0] + '  ' + marks[1] + '  ' + marks[2] + '  |',
            '|  ' + marks[3] + '  ' + marks[4] + '  ' + marks[5] + '  |',
            '|  ' + marks[6] + '  ' + marks[7] + '  ' + marks[8] + '  |',
            ' - - - - - - - - ']


def ask_for_turn():
    loc = input('Where do you want to place your marker?\n->')
    return loc


def check_input(input, boarded):
    if input.lower() == 'cancel':
        exit()
    elif input[0].lower() in ['a', 'b', 'c'] and (input[1] in ['1', '2', '3']) and input[0:2].lower() not in boarded:
        print(input[0:2].lower() + ' was chosen!')
        return True
    else:
        print(input[0:2].lower() + ' is not valid.')
        return False


def check_for_win(ai_moves, p1_moves):
    score_mat = ai_moves - p1_moves
    rows = score_mat.sum(axis=1)
    columns = score_mat.sum(axis=0)
    horiz1 = np.trace(score_mat)
    horiz2 = np.trace(np.fliplr(score_mat))
    allset = np.hstack([rows, columns, horiz1, horiz2])
    a = np.where(allset == 2)

    if allset[a].size == 0:
        return [-1, 0]
    index_win = index_it[a]
    if index_win[0] < 3:
        loc = np.where(score_mat[index_win[0]] == 0)
        return [index_win[0], index_it[loc[0]][0]]
        # exit()
    elif index_win[0] < 6:
        loc = np.where(score_mat[..., index_win[0] % 3] == 0)
        return [index_it[loc][0], index_win[0] % 3]
    elif index_win[0] == 6 or index_win[0] == 7:
        score_mat_temp2 = score_mat.copy()
        if index_win[0] == 7:
            score_mat_temp2 = np.fliplr(score_mat_temp2)
        loc = np.where(score_mat_temp2.diagonal() == 0)
        if index_win[0] == 7:
            return [index_it[loc][0], (2 * index_it[loc][0] - 1) % 3]
        else:
            return [index_it[loc][0], index_it[loc][0]]
        # quit()
    return [-1, 0]


def take_turn(moves_, chosen_, p1_mark_):
    location = ''
    location_accept = False
    cancel_tick = 0
    while location_accept is False:
        cancel_tick += 1
        if cancel_tick > 3:
            print('You can write "cancel" to end the game.\n')
        location = ask_for_turn()
        location_accept = check_input(location, chosen_)
        location = location[0:2]
    moves_[moves_.index(location.lower())] = p1_mark_
    chosen_.append(location.lower())
    print('\n'.join(fill_board(moves_)))


def how_many_wins(temp_score_mat, mark):
    temp_score_mat[mark[0], mark[1]] = 1
    rows = temp_score_mat.sum(axis=1)
    columns = temp_score_mat.sum(axis=0)
    horiz1 = np.trace(temp_score_mat)
    horiz2 = np.trace(np.fliplr(temp_score_mat))
    all_set = np.hstack([rows, columns, horiz1, horiz2])
    a = np.where(all_set == 2)
    return all_set[a].size


def find_turn(ai_moves, p1_moves):
    score_mat = ai_moves - p1_moves

    if score_mat[1, 1] == 0:
        return [1, 1]

    store_wins = np.zeros((3, 3))
    for row in range(3):
        for column in range(3):
            if score_mat[row, column] == 0:
                temp_score_mat = score_mat.copy()
                wins_num = how_many_wins(temp_score_mat, [row, column])
                # print('Wins Num is :')
                # print(wins_num)
                if wins_num > 1:
                    print('2 wins found!')
                    return [row, column]
                store_wins[row, column] = wins_num



    for i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
        if store_wins[i[0], i[1]] != 0:

            return [i[0], i[1]]

    for i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
        if store_wins[i[0], i[1]] != 0:
            return [i[0], i[1]]

    for i in [[0, 0], [0, 2], [2, 0], [2, 2], [0, 1], [1, 0], [1, 2], [2, 1]]:
        if score_mat[i[0], i[1]] == 0:
            return [i[0], i[1]]

    return [-1, 0]


def ai_turn(_moves, _chosen, _p1_mark, _ai_mark):
    p1_moves = []
    ai_moves = []
    for i in range(0, len(_moves)):
        p1_moves.append(int(_moves[i] == _p1_mark))
        ai_moves.append(int(_moves[i] == _ai_mark))
    p1_moves_mat = np.array([p1_moves[0:3], p1_moves[3:6], p1_moves[6:9]])
    ai_moves_mat = np.array([ai_moves[0:3], ai_moves[3:6], ai_moves[6:9]])
    win_check = check_for_win(ai_moves_mat, p1_moves_mat)

    if win_check[0] != -1:
        print('Win detected! ')
        print('I will take a turn at...')
        print(win_check)
        _moves[win_check[0] * 3 + (win_check[1])] = _ai_mark
        _chosen.append(index_ax[win_check[0], win_check[1]])
        print('\n'.join(fill_board(_moves)))
        return

    defend_check = check_for_win(p1_moves_mat, ai_moves_mat)

    if defend_check[0] != -1:
        print('I will take a turn at...')
        print(defend_check)
        _moves[defend_check[0] * 3 + (defend_check[1])] = _ai_mark
        _chosen.append(index_ax[defend_check[0], defend_check[1]])
        print('\n'.join(fill_board(_moves)))
        return

    # print('No issues detected')

    turn_take = find_turn(ai_moves_mat, p1_moves_mat)

    if turn_take[0] != -1:
        print('I will take a turn at...')
        print(turn_take)
        _moves[turn_take[0] * 3 + turn_take[1]] = _ai_mark
        _chosen.append(index_ax[turn_take[0], turn_take[1]])
        print('\n'.join(fill_board(_moves)))
    else:
        print('I couldn\'t figure out a turn to take :(')


if __name__ == '__main__':
    print('This is a basic Tic-Tac-Toe Game.'
          '\nLet\'s play.')

    # Initialise:
    turn = rd.randrange(0, 2)
    if turn == 0:
        ai_mark = 'O '
        p1_mark = 'X '
        print('You were assigned crosses (X)'
              '\nYou go first.')
    else:
        print('You were assigned noughts (O)'
              '\nThe AI will go first.')
        p1_mark = 'O '
        ai_mark = 'X '

    chosen = []
    no_moves = 0
    max_no_moves = 9
    moves = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']
    print('\n'.join(fill_board(moves)))
    while no_moves < max_no_moves:
        if turn == 0:
            take_turn(moves, chosen, p1_mark)
            turn = 1
        else:
            print(' ------ THE AI IS TAKING A MOVE ---------')
            ai_turn(moves, chosen, p1_mark, ai_mark)
            turn = 0
        no_moves += 1
        if no_moves >= 5:
            p1_moves = []
            ai_moves = []
            for i in range(0, len(moves)):
                p1_moves.append(int(moves[i] == p1_mark))
                ai_moves.append(int(moves[i] == ai_mark))
            p1_moves_mat = np.array([p1_moves[0:3], p1_moves[3:6], p1_moves[6:9]])
            ai_moves_mat = np.array([ai_moves[0:3], ai_moves[3:6], ai_moves[6:9]])
            score_mat_here = p1_moves_mat - ai_moves_mat
            rows = score_mat_here.sum(axis=1)
            columns = score_mat_here.sum(axis=0)
            horiz1 = np.trace(score_mat_here)
            horiz2 = np.trace(np.fliplr(score_mat_here))
            all_set = np.hstack([rows, columns, horiz1, horiz2])
            a = np.where(all_set == 3)
            b = np.where(all_set == -3)
            if all_set[a].size != 0:
                print("Player wins!")
                break
            elif all_set[b].size != 0:
                print("AI wins!")
                break
    if no_moves == 9:
        print('No-one won. Game Over.')
