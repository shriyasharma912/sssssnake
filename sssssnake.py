from tkinter import *
import random

# Game Settings
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 160  # Slower speed for better gameplay
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# Global Variables
direction = "down"
game_started = False
score = 0  # Initialize score

# Snake Class
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0]] * BODY_PARTS
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


# Food Class
class Food:
    def __init__(self):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:  # Avoid spawning food on the snake
                break
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


# Move Snake
def next_turn(snake, food):
    global direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Add new head position
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
    )
    snake.squares.insert(0, square)

    # Check if the snake eats the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Remove the tail
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        if game_started:
            window.after(SPEED, next_turn, snake, food)


# Change Direction
def change_direction(new_direction):
    global direction
    # Prevent reversing the snake's direction
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


# Check Collisions
def check_collisions(snake):
    x, y = snake.coordinates[0]
    # Wall collisions
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    # Self collisions
    for segment in snake.coordinates[1:]:
        if segment == [x, y]:
            return True
    return False


# Game Over
def game_over():
    global game_started
    game_started = False
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        text="GAME OVER",
        fill="red",
        font=("Arial", 50),
        tag="gameover",
    )
    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 50,  # Slightly below "GAME OVER"
        text="Press Space Bar to Restart",
        fill="white",
        font=("Arial", 20),
        tag="restart_message",
    )


# Start Game
def start_game(event=None):
    global game_started, snake, food, score, direction
    if not game_started:
        game_started = True
        score = 0
        direction = "down"  # Reset direction to down
        label.config(text="Score: {}".format(score))
        
        # Clear everything from the canvas before starting a new game
        canvas.delete("all")
        
        # Display the initial message
        canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2,
            text="Press Space Bar to Start",
            fill="white",
            font=("Arial", 30),
            tag="start_message",
        )
        
        # Create snake and food for the new game
        snake = Snake()
        food = Food()
        
        canvas.delete("start_message")  # Remove start message after game starts
        next_turn(snake, food)


# Replay Game
def replay():
    start_game()  # Replay by calling start_game directly


# Create Window
window = Tk()
window.title("Snake Game")

# Score Label
label = Label(window, text="Score: {}".format(score), font=("consolas", 30))
label.pack()

# Game Canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center Window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Start Message
canvas.create_text(
    GAME_WIDTH / 2,
    GAME_HEIGHT / 2,
    text="Press Space Bar to Start",
    fill="white",
    font=("Arial", 30),
    tag="start_message",
)

# Function to handle key press events
def key_press(event):
    global direction
    if event.keysym == "Left" and direction != "right":
        direction = "left"
    elif event.keysym == "Right" and direction != "left":
        direction = "right"
    elif event.keysym == "Up" and direction != "down":
        direction = "up"
    elif event.keysym == "Down" and direction != "up":
        direction = "down"


# Bind the key press event to the function
window.bind("<KeyPress>", key_press)
window.bind("<space>", start_game)

# Run Game
window.mainloop()

