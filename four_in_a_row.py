# use math library if needed
import math
import random


def get_child_boards(player, board):
    """
    Generate a list of succesor boards obtained by placing a disc 
    at the given board for a given player
   
    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that will place a disc on the board
    board: the current board instance

    Returns
    -------
    a list of (col, new_board) tuples,
    where col is the column in which a new disc is placed (left column has a 0 index), 
    and new_board is the resulting board instance
    """
    res = []
    for c in range(board.cols):
        if board.placeable(c):
            tmp_board = board.clone()
            tmp_board.place(player, c)
            res.append((c, tmp_board))
    return res


def evaluate(player, board):
    """
    This is a function to evaluate the advantage of the specific player at the
    given game board.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the specific player
    board: the board instance

    Returns
    -------
    score: float
        a scalar to evaluate the advantage of the specific player at the given
        game board
    """
    adversary = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    # Initialize the value of scores
    # [s0, s1, s2, s3, --s4--]
    # s0 for the case where all slots are empty in a 4-slot segment
    # s1 for the case where the player occupies one slot in a 4-slot line, the rest are empty
    # s2 for two slots occupied
    # s3 for three
    # s4 for four
    score = [0]*5
    adv_score = [0]*5

    # Initialize the weights
    # [w0, w1, w2, w3, --w4--]
    # w0 for s0, w1 for s1, w2 for s2, w3 for s3
    # w4 for s4
    weights = [0, 1, 4, 16, 1000]

    # Obtain all 4-slot segments on the board
    seg = []
    invalid_slot = -1
    left_revolved = [
        [invalid_slot]*r + board.row(r) + \
        [invalid_slot]*(board.rows-1-r) for r in range(board.rows)
    ]
    right_revolved = [
        [invalid_slot]*(board.rows-1-r) + board.row(r) + \
        [invalid_slot]*r for r in range(board.rows)
    ]
    for r in range(board.rows):
        # row
        row = board.row(r) 
        for c in range(board.cols-3):
            seg.append(row[c:c+4])
    for c in range(board.cols):
        # col
        col = board.col(c) 
        for r in range(board.rows-3):
            seg.append(col[r:r+4])
    for c in zip(*left_revolved):
        # slash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    for c in zip(*right_revolved): 
        # backslash
        for r in range(board.rows-3):
            seg.append(c[r:r+4])
    # compute score
    for s in seg:
        if invalid_slot in s:
            continue
        if adversary not in s:
            score[s.count(player)] += 1
        if player not in s:
            adv_score[s.count(adversary)] += 1
    reward = sum([s*w for s, w in zip(score, weights)])
    penalty = sum([s*w for s, w in zip(adv_score, weights)])
    return reward - penalty


def minimax(player, board, depth_limit):
    """
    Minimax algorithm with limited search depth.

    Parameters
    ----------
    player
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################
    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the value of the board for the player
    def value(player, board, depth_limit):
        #checks if th max depth is reached or a terminal node is reached, if so return the value of the board for the player
        if depth_limit == 0 or evaluate(player, board) > 900 or evaluate(player,board) < -900:
            return evaluate(player,board), None
        #checks what player is playing and call the fun() for that player
        if max_player == player:
            return max_value(player, board, depth_limit)
        else:
            return min_value(player, board, depth_limit)
        pass

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the max value and its placement the the player can get with the board instance
    def max_value(player, board, depth_limit):
        maxvalue = -math.inf
        # Child boards from 'board' for each piece the player can play
        maxchild_boards = get_child_boards(player, board)
        maxplacement = None
        # Finds the max  value from all child boards and the placement for that value
        for child in maxchild_boards:
            newvalue = value(2, child[1], depth_limit-1)[0]
            if newvalue > maxvalue:
                maxvalue = newvalue
                maxplacement = child[0]
        return maxvalue, maxplacement
        pass

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the min value and its placement the the player can get with the board instance
    def min_value(player, board, depth_limit):
        minvalue = math.inf
        # Child boards from 'board' for each piece the player can play
        minchild_boards = get_child_boards(player, board)
        minplacement = None
        # Finds the min  value from all child boards and the placement for that value
        for child in minchild_boards:
            newvalue = value(1, child[1], depth_limit-1)[0]
            if newvalue < minvalue:
                minvalue = newvalue
                minplacement = child[0]
        return minvalue, minplacement
        pass

    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    placement = value(next_player, board, depth_limit)[1]
###############################################################################
    return placement


def alphabeta(player, board, depth_limit):
    """
    Minimax algorithm with alpha-beta pruning.

     Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go further before stopping
    alpha: float
    beta: float
    max_player: boolean


    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################
    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the value of the board for the player
    def value(player, board, depth_limit, alpha, beta):
        # checks if th max depth is reached or a terminal node is reached, if so return the value of the board for the player
        if depth_limit == 0 or evaluate(player, board) > 900 or evaluate(player, board) < -900:
            return evaluate(player, board), None
        # checks what player is playing and call the fun() for that player
        if max_player == player:
            return max_value(player, board, depth_limit, alpha, beta)
        else:
            return min_value(player, board, depth_limit, alpha, beta)
        pass

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the max value and its placement the the player can get with the board instance
    def max_value(player, board, depth_limit, alpha, beta):
        maxvalue = -math.inf
        # Child boards from 'board' for each piece the player can play
        maxchild_boards = get_child_boards(player, board)
        maxplacement = None
        # Finds the max  value from all child boards and the placement for that value
        for child in maxchild_boards:
            newvalue = value(2, child[1], depth_limit - 1, alpha, beta)[0]
            if newvalue > maxvalue:
                maxvalue = newvalue
                maxplacement = child[0]
            alpha = max(alpha, maxvalue)
            # Checks if there was alpha greater than the beta if so break because there is a better path
            if alpha >= beta:
                break
        return maxvalue, maxplacement
        pass

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the min value and its placement the the player can get with the board instance
    def min_value(player, board, depth_limit, alpha, beta):
        minvalue = math.inf
        # Child boards from 'board' for each piece the player can play
        minchild_boards = get_child_boards(player, board)
        minplacement = None
        # Finds the min  value from all child boards and the placement for that value
        for child in minchild_boards:
            newvalue = value(1, child[1], depth_limit - 1, alpha, beta)[0]
            if newvalue < minvalue:
                print(newvalue)
                minvalue = newvalue
                minplacement = child[0]
            beta = min(beta, minvalue)
            # Checks if there was alpha greater than the beta if so break because there is a better path
            if alpha >= beta:
                break
        return minvalue, minplacement
        pass

    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    placement = value(next_player, board, depth_limit, -math.inf, math.inf)[1]
###############################################################################
    return placement


def expectimax(player, board, depth_limit):
    """
    Expectimax algorithm.
    We assume that the adversary of the initial player chooses actions
    uniformly at random.
    Say that it is the turn for Player 1 when the function is called initially,
    then, during search, Player 2 is assumed to pick actions uniformly at
    random.

    Parameters
    ----------
    player: board.PLAYER1 or board.PLAYER2
        the player that needs to take an action (place a disc in the game)
    board: the current game board instance
    depth_limit: int
        the tree depth that the search algorithm needs to go before stopping
    max_player: boolean

    Returns
    -------
    placement: int or None
        the column in which a disc should be placed for the specific player
        (counted from the most left as 0)
        None to give up the game
    """
    max_player = player
    placement = None

### Please finish the code below ##############################################
###############################################################################

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the value of the board for the player
    def value(player, board, depth_limit):
        # checks if th max depth is reached or a terminal node is reached, if so return the value of the board for the player
        if depth_limit == 0 or evaluate(player, board) > 900 or evaluate(player, board) < -900:
            return evaluate(player, board), None
        # checks what player is playing and call the fun() for that player
        if max_player == player:
            return max_value(player, board, depth_limit)
        else:
            return min_value(player, board, depth_limit)
        pass

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns the max value and its placement the the player can get with the board instance
    def max_value(player, board, depth_limit):
        maxvalue = -math.inf
        # Child boards from 'board' for each piece the player can play
        maxchild_boards = get_child_boards(player, board)
        maxplacement = None
        # Finds the max  value from all child boards and the placement for that value
        for child in maxchild_boards:
            newvalue = value(2, child[1], depth_limit - 1)[0]
            if newvalue > maxvalue:
                maxvalue = newvalue
                maxplacement = child[0]
        return maxvalue, maxplacement
        pass

    # Parameters:
    # player: the player that needs to take an action (place a disc in the game)
    # board: the current game board instance
    # depth_limit: the tree depth that the search algorithm needs to go further before stopping
    # Returns:
    # returns a random placement and its value
    def min_value(player, board, depth_limit):
        # Child boards from 'board' for each piece the player can play
        minchild_boards = get_child_boards(player, board)
        # picks a random child board
        child = random.choice(minchild_boards)
        minvalue = value(1, child[1], depth_limit-1)[0]
        minplacement = child[0]
        return minvalue, minplacement
        pass

    next_player = board.PLAYER2 if player == board.PLAYER1 else board.PLAYER1
    score = -math.inf
    placement = value(next_player, board, depth_limit)[1]
###############################################################################
    return placement


if __name__ == "__main__":
    from game_gui import GUI
    import tkinter

    algs = {
        "Minimax": minimax,
        "Alpha-beta pruning": alphabeta,
        "Expectimax": expectimax
    }

    root = tkinter.Tk()
    GUI(algs, root)
    root.mainloop()
