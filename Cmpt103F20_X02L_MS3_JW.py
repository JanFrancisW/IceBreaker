from graphics import *
import math
import time 

# Jan Walicki
# Ice Breakers
# Click run to play.

       

# Purpose:  To determine if the users click is an on adjacent square to the players location.
# Parameters: player-> the player 1 or 2 image object... click-> the Point object from the users click
# Return: True is the click is adjacent.False if it is not.
def adjacent(player, click):
    if player[0] == click[0] and (player[1] == click[1] + 1 or player[1] == click[1] - 1):
        return True
    elif (player[0] == click[0] + 1 or player[0] == click[0] - 1) and (player[1] == click[1] or player[1] == click[1] + 1 or player[1] == click[1] - 1):
        return True
    else:
        return False

# Purpose:  To create the board by drawing a 10 x 8 grid of reactangles.
# Parameters: 'win' the graphics window from the main function.
# Return: It returns the the board.
def create_board(win):
    board = []
    
    for i in range(10):
        square_list = []
        for j in range(8):
            square = Rectangle(Point(i * 60, j * 60), Point((i + 1) * 60, (j + 1) * 60))
            square.draw(win)
            square_list.append(square)
        board.append(square_list)
    
    return board

# Purpose:  To create the players and load their images to their starting points.
# Parameters: 'win' the graphics window from the main function.
# Return: player 1 and player 2.
def create_players(win, point1, point2):
    player1 = Image(point1, "Player_Brutus.gif")
    player1.draw(win)
    player2 = Image(point2, "Player_Popeye.gif")
    player2.draw(win)
    return player1, player2

# Purpose:  To create a text window to display messages.
# Parameters: 'win' the graphics window from the main function,
#             'message' - a string to display in the message area.
# Return: It returns the rectangle objects for both the quit and reset buttons.
def create_message(win, message):
    main_msg = Text(Point(75, 575), message)
    main_msg.draw(win)
    return main_msg

# Purpose:  To create a quit and reset button to display.
# Parameters: 'win' the graphics window from the main function.
# Return: It returns the rectangle objects for both the quit and reset buttons.
def create_buttons(win):
    quit_rect = Rectangle(Point(475, 525), Point(575, 555))
    quit_text = Text(Point(525, 540), "QUIT").draw(win)
    quit_rect.draw(win)
    
    reset_rect = Rectangle(Point(475, 560), Point(575, 590))
    reset_text = Text(Point(525, 575), "RESET").draw(win) 
    reset_rect.draw(win)
    return quit_rect, reset_rect

# Purpose:  To determine if a mouse click was within a rectangle.
# Parameters: pt - a point from a click, r, a rectangle object.
# Return: True if pt is in the rectangle.
def in_Rectangle(pt, r):
    x = pt.getX()
    y = pt.getY()
    rect_P1 = r.getP1()
    rect_P2 = r.getP2()
    x_P1 = rect_P1.getX()
    y_P1 = rect_P1.getY()
    x_P2 = rect_P2.getX()
    y_P2 = rect_P2.getY()  
    if x >= x_P1 and x <= x_P2 and y >= y_P1 and y <= y_P2:
        return True
    
# Purpose:  To get the column and row from a player object.
# Parameters: The player object. Either player1 or player2.
# Return: The column and the row where the player is located.
def coordinates_of_player(player):
    center = player.getAnchor()
    x = center.getX()
    y = center.getY()    
    row = (y // 60) + 1
    column = (x // 60) + 1 
    return row, column
    
# Purpose:  To get the column and row from a click.
# Parameters: The point object from a mouse click. 
# Return: The column and the row where the click took place.
def coordinates_of_click(point):
    x = point.getX()
    y = point.getY()
    row = (y // 60) + 1
    column = (x // 60) + 1
    return row, column

# Purpose:  To determine which players turn it is to move and break ice. The players are
#           moved around the board by undrawing them and redrawing them if moves are valid.
#           The square objects are changed to a blue fill if it is a valid square.
#
# Parameters: turn         -> an integer from 0-3: 0 is players1 move, 1 player1 to break ice etc..
#             player1      -> image object that will be moved around the board
#             player2      -> image object that will be moved around the board
#             coordinates  -> The row and column of the players click on the board
#             player1_coord-> The current row and column of player1
#             player2_coord-> The current row and column of player2
#             main_msg     -> The message that displays below the game board
#             square       -> A rectangle object that can be white, blue, or have a player object overtop of itself.
#             win          -> The main gameplay graphic window.
#             row          -> The row of a mouse click.
#             column       -> The column of a mouse click.
# Return: It returns the player objects, and the numerical value turn.
def turn_play(turn, player1, player2, coordinates, player1_coord, player2_coord, main_msg, square, win, row, column):
    if turn == 0:
        if (adjacent(player1_coord, coordinates) == True) and square.config["fill"] != "blue":
            p2_location = player2.getAnchor()
            player1.undraw()
            player2.undraw()
            player1, player2 = create_players(win, Point((column * 60)-30, (row * 60)-30), p2_location)
            
            main_msg.setText("Click to break ice.")
            turn += 1 
            return turn, player1, player2
            
        else:
            main_msg.setText("Invalid move, click again")
            return turn, player1, player2
    if turn == 1:
        if square.config["fill"] != "blue" and player1_coord != coordinates and player2_coord != coordinates:
            square.setFill("blue") 
            turn += 1
            main_msg.setText("Player 2 it's your turn")
            return turn, player1, player2
        else:
            main_msg.setText("Invalid move: click again")
            return turn, player1, player2
    
    if turn == 2:
        if (adjacent(player2_coord, coordinates) == True) and square.config["fill"] != "blue":
            p1_location = player1.getAnchor()
            player1.undraw()
            player2.undraw()
            player1, player2 = create_players(win, p1_location, Point((column * 60)-30, (row * 60)-30))
            
            main_msg.setText("Click to break ice.")
            turn += 1 
            return turn, player1, player2
        else:
            main_msg.setText("Invalid move, click again")
            return turn, player1, player2
    if turn == 3:
        if square.config["fill"] != "blue" and player1.getAnchor() != square.getCenter() and player2.getAnchor() != square.getCenter():
            square.setFill("blue") 
            turn = 0
            main_msg.setText("Player 1 it's your turn")
            return turn, player1, player2    
        else:
            main_msg.setText("Invalid move: click again")
            return turn, player1, player2        
        
# Purpose:  To create a play and exit button to display in the opening window.
# Parameters: 'opening_win' the graphics window that precedes the game window opening.
# Return: It returns the rectangle objects for both the play and exit buttons.
def create_opening_buttons(opening_win):
    play_rect = Rectangle(Point(50, 50), Point(100, 70))
    play_text = Text(Point(75, 60), "PLAY").draw(opening_win)
    play_rect.draw(opening_win)
    
    exit_rect = Rectangle(Point(50, 80), Point(100, 100))
    exit_text = Text(Point(75, 90), "EXIT").draw(opening_win) 
    exit_rect.draw(opening_win)
    return play_rect, exit_rect


def is_trapped(player1_coord, player2_coord, board):
    r,c = player1_coord
    adjacent_squares = [(r -1, c), (r + 1, c), (r, c + 1), (r, c - 1), (r -1, c + 1), (r-1, c-1), (r +1, c +1), (r +1, c -1)]
    count = 0
    if player2_coord in adjacent_squares:
        adjacent_squares.remove(player2_coord)
    for square in adjacent_squares:
        if board[square[0]][square[1]].config["fill"] == "white":
            count += 1
    if count >= 1:
        return False
    else:
        return True
    
# Purpose:  This function must be called to run the game.
# Parameters: none 
# Return: none.
def main():
    opening_win = GraphWin('', 150, 150)
    opening_win.setBackground("maroon")
    opening_message = Text(Point(75, 25), "Welcome to Ice Breakers").draw(opening_win)
    play, exit = create_opening_buttons(opening_win)
    click_point = opening_win.getMouse()
    if in_Rectangle(click_point, exit):
        opening_win.close()
    elif in_Rectangle(click_point, play):
        opening_win.close()
    
        win = GraphWin('Jan Walicki -- Ice Breakers', 600, 650)
        quit, reset = create_buttons(win)
        main_msg = create_message(win, 'Player 1')
        board = create_board(win)
        player1, player2 = create_players(win, Point(30, 270), Point(570, 270))
        turn = 0
    
    
        while True:
            try:
                pt = win.getMouse()
                           
            except:
                win.close()
                
            x = pt.getX()
            y = pt.getY()
            row = (y // 60) + 1
            column = (x // 60) + 1
            row_column_tuple = "(" + str(column) + ", " + str(row) + ")"
            
            
            if y < 480:
                
                square = board[column-1][row-1]
                player1_coord = coordinates_of_player(player1)
                player2_coord = coordinates_of_player(player2)           
                coordinates = coordinates_of_click(pt)
                
                turn1, player1, player2 = turn_play(turn, player1, player2, coordinates, player1_coord, player2_coord, main_msg, square, win, row, column)
                turn = turn1
                player1_post_move = coordinates_of_player(player1)
                player2_post_move = coordinates_of_player(player2)
                player1_trapped = is_trapped(player1_post_move, player2_post_move, board)
                #player2_trapped = is_trapped(player2_post_move, player1_post_move, board)
            
            if in_Rectangle(pt, quit) == True:    
                main_msg.setText("byebye")
                time.sleep(1)
                win.close()
            elif in_Rectangle(pt, reset) == True:
                main_msg.setText("game resetting")
                player1.undraw()
                player2.undraw()
                turn = 0
                player1, player2 = create_players(win, Point(30, 270), Point(570, 270))
                for i in range(10):
                    for j in range(8):
                        board[i][j].setFill('white')
            elif y > 480:
                location = "(" + str(x) + ", " + str(y) + ")"
                main_msg.setText(location)
            
main()