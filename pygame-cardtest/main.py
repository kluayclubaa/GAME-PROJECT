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
background_img = pygame.image.load('background/background.png')
pull_img = pygame.image.load('background/legendary1.png')
gacha_background=pygame.image.load('gacha background/1.jpg')

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
next_button_rect = pygame.Rect((1300,800, button_width, button_height))

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
SHOW_STATE="show_State"
SHOWTEN_STATE="show_ten_State"
WHENTEN_PULLED="when_ten_pulled"
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
    input_box_rect = pygame.Rect(SCREEN_WIDTH - 500, 70, 300, 100)  # Centered input box
    pygame.draw.rect(screen, (255, 255, 255), input_box_rect, border_radius=10)  # White background

    text_prompt = font_coin.render("Enter Code:", True, BLACK)
    screen.blit(text_prompt, (input_box_rect.x + 10, input_box_rect.y + 10))  # Position the prompt text
    
    # Code entry text rendering (assuming a variable 'input_text' stores the current input)
    code_text = font_coin.render(input_text, True, BLACK)
    screen.blit(code_text, (input_box_rect.x + 10, input_box_rect.y + 50))  # Position the user input

input_text = ""  # Stores the user's code input
code_active = False  # Tracks if the input box is currently active
correct_code = ["ASIA","HAM888","DUELSTARIMPACT","HAMXAOMAKKUB"]  # Define the correct code here
code_used = []  # Boolean to track if the correct code has been used
message = ""  # Message to show feedback ("Code used", "Wrong code", etc.)
message_timer = 0  # Timer for how long the message should be shown


def handle_code_entry(event, coin):
    global input_text, code_active, correct_code, code_used, message, message_timer
    if code_active:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Press Enter to submit the code
                if input_text in correct_code :
                    coin += 1000  # Increase coin by 1000 if the correct code is entered
                    code_used.append(input_text)  # Mark the code as used
                    correct_code.remove(input_text)
                    message = "successfully!"
                    
                    message_timer = pygame.time.get_ticks()  # Start the message timer
                elif input_text in code_used:
                    message = "already used!"  # Inform that the code has been used
                    message_timer = pygame.time.get_ticks()  # Start the message timer
                else:
                    message = "Wrong code!"  # Inform the user the code is wrong
                    message_timer = pygame.time.get_ticks()  # Start the message timer
                
                input_text = ""  # Reset input text after submission
                code_active = False  # Close the code input box

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]  # Remove last character on backspace
            else:
                input_text += event.unicode  # Append typed character
    return coin
def draw_message():
    """Display a temporary message for a short time after entering a code."""
    global message, message_timer
    if message:
        current_time = pygame.time.get_ticks()
        if current_time - message_timer < 1000:  # Display the message for 2 seconds
            text_surface = font_coin.render(message, True, (255, 0, 0))  # Red message
            screen.blit(text_surface, (SCREEN_WIDTH - 400, 50))
        else:
            message = ""  # Clear the message after 2 seconds

pull_couse=100
ten_pull_couse=1000
tenshow=[]
current_card_index = 0
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
                elif pull_button_rect.collidepoint(event.pos) and coin>=pull_couse:
                    pulled_card = gacha.pull()
                   
                    game_state = SHOW_STATE
                    
                    if pull_button_rect.collidepoint(event.pos):
                        coin-=100
                        
                        
                elif Ten_pills_button_rect.collidepoint(event.pos) and coin>=ten_pull_couse:
                    for i in range(10):
                        pulled_card = gacha.pull()
                        tenshow.append(pulled_card.show)
                    game_state = SHOWTEN_STATE
                    if Ten_pills_button_rect.collidepoint(event.pos):
                        coin-=1000
                    
            elif game_state == WHEN_PULLED:
                if exit_button_rect.collidepoint(event.pos):
                    game_state = GACHA
                elif plus_button_rect.collidepoint(event.pos):
                    code_active = True
                elif pull_button_rect.collidepoint(event.pos) and coin>=pull_couse:
                    pulled_card = gacha.pull()
                    
                    game_state = SHOW_STATE
                    
                    if pull_button_rect.collidepoint(event.pos):
                        coin-=100
                        
                elif Ten_pills_button_rect.collidepoint(event.pos) and coin>=ten_pull_couse:
                    for i in range(10):
                        pulled_card = gacha.pull()
                        tenshow.append(pulled_card.show)
                    game_state = SHOWTEN_STATE
                    if Ten_pills_button_rect.collidepoint(event.pos):
                        coin-=1000
            elif game_state == SHOWTEN_STATE:
                # if next_button_rect.collidepoint(event.pos):
                #     current_card_index = (current_card_index + 1) 
                    
                if event.button == 1:
                    current_card_index+=1
                    if current_card_index >= len(tenshow):
                        game_state = WHEN_PULLED
            elif game_state== SHOW_STATE:
                if event.button == 1:
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
        screen.blit(pull_img, (50, 0))
        draw_coin_box(coin)
        plus_button_rect = draw_coin_box(coin)
        mouse_pos = pygame.mouse.get_pos()
        draw_button(exit_button_rect, "Exit", exit_button_rect.collidepoint(mouse_pos))
        draw_button(pull_button_rect, "Pull", pull_button_rect.collidepoint(mouse_pos))
        draw_button(Ten_pills_button_rect, "10 Pulls", Ten_pills_button_rect.collidepoint(mouse_pos))
        if code_active:
            draw_code_input_box()

        draw_message()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME

    elif game_state == COLLECTION:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME
    elif game_state == WHEN_PULLED:
        resize_gacha_background=pygame.transform.scale(gacha_background,(SCREEN_WIDTH-150,SCREEN_HEIGHT))
        screen.blit(resize_gacha_background,(75,0))
        draw_button(exit_button_rect, "Exit", exit_button_rect.collidepoint(mouse_pos))
        draw_button(pull_button_rect, "Pull", pull_button_rect.collidepoint(mouse_pos))
        draw_button(Ten_pills_button_rect, "10 Pulls", Ten_pills_button_rect.collidepoint(mouse_pos))
        draw_coin_box(coin)
        if code_active:
            draw_code_input_box()
        draw_message()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME

    elif game_state == SHOW_STATE:
        resize_show_card=pygame.transform.scale(pulled_card.show,(1550,900))
        screen.blit(resize_show_card, (180, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            game_state = WHEN_PULLED
    elif game_state == SHOWTEN_STATE:
       
        if tenshow:
            resize_show_card=pygame.transform.scale(tenshow[current_card_index],(1550,900))
        
            screen.blit(resize_show_card, (180, 0))
        
        
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            game_state = WHEN_PULLED
        
        

    pygame.display.update()
    clock.tick(30)

pygame.quit()