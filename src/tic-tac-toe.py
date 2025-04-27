import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 40)  # Dark background
CONTAINER_COLOR = (50, 50, 60)  # Slightly lighter container
CONTAINER_SIZE = 400  # Square container
LINE_COLOR = (200, 200, 200)  # Light gray for grid lines
LINE_WIDTH = 4  # Width of the grid lines
TEXT_COLOR = (255, 255, 255)  # White for text
BUTTON_COLOR = (70, 70, 90)  # Button color
BUTTON_TEXT_COLOR = (255, 255, 255)  # Button text color
TITLE_COLOR = (255, 105, 108) # Title color 
WIN_ANIMATION_DURATION = 1000  # 1 second for animation
win_animation_start = 0
is_animating_win = False
BOT_MOVE_DELAY = 800  # 0.8 second delay before bot moves
last_move_time = 0

# Screen states 
START_SCREEN = 0 
GAME_SCREEN = 1
GAME_OVER_SCREEN = 2 
current_screen = START_SCREEN
selected_opponent = None


class GameState:
    def __init__(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.current_player = "X"
        self.winner = None
        self.game_over = False
        self.winning_cells = []
    
    def make_move(self, row, col):
        """Make a move on the board"""
        if not self.game_over and self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.check_winner()
            if not self.game_over:
                self.switch_player()
            return True
        return False
    
    def switch_player(self):
        """Switch the current player"""
        self.current_player = "O" if self.current_player == "X" else "X"
    
    def check_winner(self):
        """Check if the current player has won"""
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                self.set_winner(self.board[row][0], [(row, 0), (row, 1), (row, 2)])
                return
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                self.set_winner(self.board[0][col], [(0, col), (1, col), (2, col)])
                return
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.set_winner(self.board[0][0], [(0, 0), (1, 1), (2, 2)])
            return
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.set_winner(self.board[0][2], [(0, 2), (1, 1), (2, 0)])
            return
        
        # Check for draw
        if all(cell != "" for row in self.board for cell in row):
            self.game_over = True
    
    def set_winner(self, winner, winning_cells):
        """Set the winner and winning cells"""
        self.winner = winner
        self.winning_cells = winning_cells
        self.game_over = True
    
    def reset(self):
        """Reset the game state"""
        self.__init__()
        
    # Adding bot logic here      
    def is_terminal(self):
        """Check if game is over"""
        return self.game_over

    def get_available_moves(self):
        """Return list of (row,col) for empty cells"""
        return [(r,c) for r in range(3) for c in range(3) if self.board[r][c] == ""]

    def evaluate(self):
        """Score the current board state"""
        if self.winner == "O":  # Assuming O is bot
            return 1
        elif self.winner == "X":
            return -1
        return 0
    
    def copy(self):
        """Create a deep copy of the game state"""
        new_state = GameState()
        new_state.board = [row[:] for row in self.board]
        new_state.current_player = self.current_player
        new_state.winner = self.winner
        new_state.game_over = self.game_over
        new_state.winning_cells = self.winning_cells[:]
        return new_state    

def minimax(game_state, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm implementation
    Returns the evaluation score of the board state
    """
    if game_state.is_terminal() or depth == 0:
        return game_state.evaluate()
    
    if is_maximizing:  # Bot's turn (O)
        max_eval = -float('inf')
        for move in game_state.get_available_moves():
            new_state = game_state.copy()
            new_state.make_move(*move)
            eval = minimax(new_state, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # alpha beta prunning 
                break
        return max_eval
    else:  # Player's turn (X)
        min_eval = float('inf')
        for move in game_state.get_available_moves():
            new_state = game_state.copy()
            new_state.make_move(*move)
            eval = minimax(new_state, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: # alpha beta pruning 
                break 
        return min_eval

def get_bot_move(game_state):
    """
    Uses minimax to find the best move for the bot
    Returns (row, col) of the best move
    """
    best_score = -float('inf')
    best_move = None
    alpha = -float("inf")
    beta = float("inf")
    
    for move in game_state.get_available_moves():
        new_state = game_state.copy()
        new_state.make_move(*move)
        score = minimax(new_state, 5, alpha, beta, False)  # Depth 5 is sufficient for tic-tac-toe
        
        if score > best_score:
            best_score = score
            best_move = move
            alpha = max(alpha, score)  # update the alpha with the best score found so far 
    return best_move

def draw_start_screen():
    """Draw the opponent selection screen"""
    screen.fill(BG_COLOR)
    
    font = pygame.font.SysFont('Orbitron', 45)
    # Title
    title = font.render("Choose Your Opponent", True, TITLE_COLOR)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Opponent buttons
    button_width, button_height = 200, 50
    buttons = []
    
    # Friend button
    friend_rect = pygame.Rect(
        WIDTH//2 - button_width//2,     # 800 // 2 = 400, 400 - 200 // 2 =  400 - 100 = 300 (x cordinate)
        HEIGHT//2 - button_height,      # 600 // 2 = 300, 300 - 50 // 2 = 300 - 25 = 275 (y coardinate)
        button_width,
        button_height
    )
    pygame.draw.rect(screen, BUTTON_COLOR, friend_rect, border_radius=5)
    friend_text = font.render("Friend", True, BUTTON_TEXT_COLOR)
    friend_text_rect = friend_text.get_rect(center=friend_rect.center)
    screen.blit(friend_text, friend_text_rect)
    buttons.append(("friend", friend_rect))
    
    # Bot button
    bot_rect = pygame.Rect(
        WIDTH//2 - button_width//2,   #  300  (x cordinate)
        HEIGHT//2 + 20,               # 325  (y coardinate)
        button_width,
        button_height
    )
    pygame.draw.rect(screen, BUTTON_COLOR, bot_rect, border_radius=5)
    bot_text = font.render("Bot", True, BUTTON_TEXT_COLOR)
    bot_text_rect = bot_text.get_rect(center=bot_rect.center)
    screen.blit(bot_text, bot_text_rect)
    buttons.append(("bot", bot_rect))
    
    return buttons

def draw_game_screen():
    """Draw the game board with current turn indicator"""
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont('Orbitron', 40)
    # Draw turn indicator
    turn_text = f"{game_state.current_player}'s Turn" if selected_opponent == "friend" else f"Your Turn" if game_state.current_player == "X" else "Bot's Turn"
    turn_surface = font.render(turn_text, True, TEXT_COLOR)
    screen.blit(turn_surface, ((WIDTH - CONTAINER_SIZE) // 2 + (CONTAINER_SIZE  - 250), 35)) # set the turn text placement here 
    
    # Draw game container
    container_rect = pygame.Rect(
        (WIDTH - CONTAINER_SIZE) // 2,
        (HEIGHT - CONTAINER_SIZE) // 2,
        CONTAINER_SIZE,
        CONTAINER_SIZE
    )
    pygame.draw.rect(screen, CONTAINER_COLOR, container_rect)
    draw_grid(container_rect)
        
def draw_grid(container_rect):
    """Draw the tic-tac-toe grid lines inside the container"""
    # Calculate cell size (each square will be 1/3 of container size)
    cell_size = CONTAINER_SIZE // 3
    
    # Draw vertical lines
    for i in range(1, 3):
        x = container_rect.left + i * cell_size
        pygame.draw.line(
            screen, 
            LINE_COLOR, 
            (x, container_rect.top), 
            (x, container_rect.bottom), 
            LINE_WIDTH
        )
    
    # Draw horizontal lines
    for i in range(1, 3):
        y = container_rect.top + i * cell_size
        pygame.draw.line(
            screen, 
            LINE_COLOR, 
            (container_rect.left, y), 
            (container_rect.right, y), 
            LINE_WIDTH
        )
    # Draw X's and O's
    symbol_font = pygame.font.SysFont('arial', 100)
    for row in range(3):
        for col in range(3):
            if game_state.board[row][col] != "":
                text = symbol_font.render(game_state.board[row][col], True, TEXT_COLOR)
                text_rect = text.get_rect(
                    center=(
                        container_rect.left + col * cell_size + cell_size//2,
                        container_rect.top + row * cell_size + cell_size//2
                    )
                )
                screen.blit(text, text_rect)
    # Handle win animation
    if is_animating_win and game_state.winning_cells:
        # Calculate animation progress (0 to 1)
        progress = min(1.0, (pygame.time.get_ticks() - win_animation_start) / (WIN_ANIMATION_DURATION * 0.8))
        # Get start and end points
        start_row, start_col = game_state.winning_cells[0]
        end_row, end_col = game_state.winning_cells[-1]
        
        # Calculate positions
        start_x = container_rect.left + start_col * cell_size + cell_size//2
        start_y = container_rect.top + start_row * cell_size + cell_size//2
        end_x = container_rect.left + end_col * cell_size + cell_size//2
        end_y = container_rect.top + end_row * cell_size + cell_size//2
        
        # Current line end based on progress
        current_x = start_x + (end_x - start_x) * progress
        current_y = start_y + (end_y - start_y) * progress
        
        # Draw the animated line
        pygame.draw.line(
            screen, 
            (0, 255, 0),  # Bright green
            (start_x, start_y), 
            (current_x, current_y), 
            LINE_WIDTH * 2
        )
                
def draw_game_over():
    """Draw the game over screen with appropriate message"""
    # Clear screen
    screen.fill(BG_COLOR)
    
    # Determine message
    if game_state.winner:
        message = f"Player {game_state.winner} Wins!"
    else:
        message = "It's a Draw!"
        
    # Draw message
    font = pygame.font.SysFont('Orbitron', 72)
    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text, text_rect)
    
    # Draw restart button
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=5)
    
    # Button text
    button_font = pygame.font.SysFont('Orbitron', 32)
    button_text = button_font.render("Restart", True, BUTTON_TEXT_COLOR)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    return button_rect  # Return for future click detection

# Game state 
game_state = GameState()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe 💙")

def main():
    global current_screen, selected_opponent,is_animating_win
    
    clock = pygame.time.Clock()
    container_rect = pygame.Rect(
        (WIDTH - CONTAINER_SIZE) // 2,
        (HEIGHT - CONTAINER_SIZE) // 2,
        CONTAINER_SIZE,
        CONTAINER_SIZE
    )
    
    while True:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == START_SCREEN:
                    buttons = draw_start_screen() # return (shows the Bot and Friend button to choose the opponent)
                    for opponent_type, rect in buttons:
                        if rect.collidepoint(mouse_pos):
                            selected_opponent = opponent_type
                            current_screen = GAME_SCREEN
                            game_state.reset()
                            
                elif current_screen == GAME_SCREEN and not is_animating_win:
                    # Calculate which cell was clicked
                    relative_x = mouse_pos[0] - container_rect.left
                    relative_y = mouse_pos[1] - container_rect.top
                    cell_size = CONTAINER_SIZE // 3
                    
                    if 0 <= relative_x < CONTAINER_SIZE and 0 <= relative_y < CONTAINER_SIZE:
                        col = int(relative_x // cell_size)
                        row = int(relative_y // cell_size)
                        
                        if game_state.make_move(row, col):
                            last_move_time = pygame.time.get_ticks()  # Start the bot delay timer
                            if game_state.game_over:
                                win_animation_start = current_time
                                is_animating_win = True
                                                    
                elif current_screen == GAME_OVER_SCREEN:
                        button_rect = draw_game_over() # return a button to restart the game
                        if button_rect.collidepoint(mouse_pos):
                            # Reset the game state 
                            current_screen = START_SCREEN
                            selected_opponent = None
                            game_state.reset()
        
        # Add bot move handling 
        if (current_screen == GAME_SCREEN and selected_opponent == "bot" and game_state.current_player == "O" and not is_animating_win
            and current_time - last_move_time > BOT_MOVE_DELAY):
            row, col = get_bot_move(game_state)
            if game_state.make_move(row, col) and game_state.game_over:
                win_animation_start = current_time
                is_animating_win = True
            last_move_time = current_time  # Reset the timer
                            
        # Check if animation should end
        if is_animating_win and current_time - win_animation_start > WIN_ANIMATION_DURATION:
            current_screen = GAME_OVER_SCREEN
            is_animating_win = False   
                
        # Draw the appropriate screen 
        if current_screen == START_SCREEN:
            draw_start_screen()
        elif current_screen == GAME_SCREEN:
            draw_game_screen()
        elif current_screen == GAME_OVER_SCREEN:
            draw_game_over()
                    
        # Update the display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()

# In your game code (temporarily add):
pygame.image.save(screen, "screenshot.png")