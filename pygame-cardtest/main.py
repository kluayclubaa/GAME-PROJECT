import pygame
from gacha import GachaSystem  # Import your Gacha system
from ai_battle import AIBattle  # Import your Battle system
from deck import Deck  # Import Deck system
from collection import Collection  # Import Collection system

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (50, 50, 100)
HOVER_COLOR = (100, 100, 200)
background_img = pygame.image.load('back ground/background.png')
pull_img = pygame.image.load('back ground/gacha.png')

# Load the coin image
coin_img = pygame.image.load('asset/coin.png')  # Path to your coin image
coin_img = pygame.transform.scale(coin_img, (30, 30))  # Resize the coin image if necessary

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game Home Page")

font = pygame.font.Font(pygame.font.match_font('impact'), 60)
font_coin=pygame.font.Font(pygame.font.match_font('MN Pu Khem'),32)

# Button setup
button_width, button_height = 400, 50
battle_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 500, button_width, button_height))
deck_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 600, button_width, button_height))
gacha_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 700, button_width, button_height))
exit_button_rect = pygame.Rect((1300, 800, button_width, button_height))
pull_button_rect = pygame.Rect((200, 800, button_width, button_height))
collection_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 800, button_width, button_height))
Ten_pills_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 800, button_width, button_height))

# Initialize systems
gacha = GachaSystem()  # Initialize the Gacha system
collection = Collection()  # Initialize the Collection system
deck = Deck(collection)  # Pass the Collection object to Deck
ai_battle = AIBattle()  # Initialize the AI Battle system

# Initialize variables for displaying pulled card result
pulled_card = None
pulled_card_time = None

# Define card display size
CARD_WIDTH, CARD_HEIGHT = 200, 300  # Desired card image size

# Game states
HOME = "home"
BATTLE = "battle"
DECK = "deck"
GACHA = "gacha"
COLLECTION = "collection"
WHEN_PULLED = "when_pulled"
game_state = HOME

clock = pygame.time.Clock()

# Function to draw buttons on the home page
def draw_button(rect, text, hovered=False):
    color = HOVER_COLOR if hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)
    text_render = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(text_render, (rect.x + (rect.width - text_render.get_width()) // 2, rect.y + (rect.height - text_render.get_height()) // 2))

def draw_coin_box(coin_amount):
    """Draw the coin box on the top-right corner of the screen with a + button for adding coins."""
    # Define the dimensions and layout for the coin box
    coin_box_rect = pygame.Rect(SCREEN_WIDTH - 400, 20, 150, 40)  # Larger width to fit the '+' button
    pygame.draw.rect(screen, (220, 220, 220), coin_box_rect, border_radius=20)  # Light background for the coin box

    # Render the coin amount text
    coin_text = font_coin.render(f"{coin_amount}", True, BLACK)
    
    # Position for coin image and coin text
    screen.blit(coin_img, (SCREEN_WIDTH - 400, 25))  # Position the coin image
    screen.blit(coin_text, (SCREEN_WIDTH - 370, 12))  # Position the coin amount text

    # Draw the "+" button next to the coin amount
    plus_button_rect = pygame.Rect(SCREEN_WIDTH - 290, 25, 30, 30)  # Position of the '+' button
    pygame.draw.rect(screen, (255, 255, 255), plus_button_rect, border_radius=25)  # White rounded button
    plus_text = font_coin.render("+", True, BLACK)
    screen.blit(plus_text, (SCREEN_WIDTH - 285, 10))  # Center the "+" sign within the button

    return plus_button_rect  # Return the rect of the '+' button for event detection

def timer(current_time, duration, time):
    if current_time - time < duration:
        return True
    else:
        return False

coin = 5000  # Initial coin value

def draw_code_input_box():
    """Draw the input box for entering a code to add coins."""
    input_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 100)  # Centered input box
    pygame.draw.rect(screen, (255, 255, 255), input_box_rect, border_radius=10)  # White background

    text_prompt = font_coin.render("Enter Code:", True, BLACK)
    screen.blit(text_prompt, (input_box_rect.x + 10, input_box_rect.y + 10))  # Position the prompt text
    
    # Code entry text rendering (assuming a variable 'input_text' stores the current input)
    code_text = font_coin.render(input_text, True, BLACK)
    screen.blit(code_text, (input_box_rect.x + 10, input_box_rect.y + 50))  # Position the user input

input_text = ""  # Stores the user's code input
code_active = False  # Tracks if the input box is currently active

correct_code = "ASIA"  # Define the correct code here

def handle_code_entry(event, coin):
    global input_text, code_active
    if code_active:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to submit the code
                if input_text == correct_code:
                    coin += 1000  # Increase coin by 1000 if the correct code is entered
                input_text = ""  # Reset input text after submission
                code_active = False  # Close the code input box
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  # Remove last character on backspace
            else:
                input_text += event.unicode  # Append typed character
    return coin


# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == HOME:
                if battle_button_rect.collidepoint(event.pos):
                    game_state = BATTLE
                elif deck_button_rect.collidepoint(event.pos):
                    game_state = DECK
                elif gacha_button_rect.collidepoint(event.pos):
                    game_state = GACHA
                elif collection_button_rect.collidepoint(event.pos):
                    game_state = COLLECTION
            elif game_state == GACHA:
                if exit_button_rect.collidepoint(event.pos):
                    game_state = HOME
                elif plus_button_rect.collidepoint(event.pos):
                    code_active = True
                elif pull_button_rect.collidepoint(event.pos):
                    game_state = WHEN_PULLED
        coin = handle_code_entry(event, coin)

    # Display home screen
    if game_state == HOME:
        screen.blit(background_img, (0, 0))
        

        mouse_pos = pygame.mouse.get_pos()
        draw_button(battle_button_rect, "Battle", battle_button_rect.collidepoint(mouse_pos))
        draw_button(deck_button_rect, "Deck", deck_button_rect.collidepoint(mouse_pos))
        draw_button(gacha_button_rect, "Gacha", gacha_button_rect.collidepoint(mouse_pos))
        draw_button(collection_button_rect, "Collection", collection_button_rect.collidepoint(mouse_pos))

    elif game_state == BATTLE:
        screen.fill(WHITE)
        text = font.render("Battle Screen - Press ESC to return", True, BLACK)
        screen.blit(text, (100, 100))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME

    elif game_state == DECK:
        screen.fill(WHITE)
        text = font.render("Deck Screen - Press ESC to return", True, BLACK)
        screen.blit(text, (100, 100))
        deck.show_deck()  # Show the current deck
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME

    elif game_state == GACHA:
        screen.blit(pull_img, (0, 0))
        draw_coin_box(coin)
        plus_button_rect = draw_coin_box(coin)
        mouse_pos = pygame.mouse.get_pos()
        draw_button(exit_button_rect, "Exit", exit_button_rect.collidepoint(mouse_pos))
        draw_button(pull_button_rect, "Pull", pull_button_rect.collidepoint(mouse_pos))
        draw_button(Ten_pills_button_rect, "10 Pulls", Ten_pills_button_rect.collidepoint(mouse_pos))
        if code_active:
            draw_code_input_box()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME

    elif game_state == COLLECTION:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME
    elif game_state == WHEN_PULLED:
        screen.fill(WHITE)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
