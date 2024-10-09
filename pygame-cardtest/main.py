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

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game Home Page")

font = pygame.font.Font(pygame.font.match_font('impact'), 60)

# Button setup
button_width, button_height = 400, 50
battle_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 500, button_width, button_height))
deck_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 600, button_width, button_height))
gacha_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 700, button_width, button_height))
exit_button_rect = pygame.Rect((1300, 600, button_width, button_height))
pull_button_rect = pygame.Rect((200, 600, button_width, button_height))
collection_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 800, button_width, button_height))
Ten_pills_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 600, button_width, button_height))

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
    
    # Drawing the button with rounded edges (optional)
    pygame.draw.rect(screen, color, rect, border_radius=12)
    
    # Adding a space-themed outer glow (optional)
    if hovered:
        glow_rect = pygame.Rect(rect.x - 5, rect.y - 5, rect.width + 10, rect.height + 10)
        pygame.draw.rect(screen, HOVER_COLOR, glow_rect, border_radius=15)
    
    # Render and position the text inside the button
    text_render = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(text_render, (rect.x + (rect.width - text_render.get_width()) // 2, 
                              rect.y + (rect.height - text_render.get_height()) // 2))

def timer(current_time, duration, time):
    
    if current_time - time < duration:
        return True
    else:
        return False



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
                elif pull_button_rect.collidepoint(event.pos):
                    game_state = WHEN_PULLED
                    # Pull a card
                    # pulled_card = gacha.pull()
                    # pulled_card_time = pygame.time.get_ticks()  # Store the current time
                    # print(f"Pulled card: {pulled_card.name} - Power: {pulled_card.power} - Rarity: {pulled_card.rarity}")
                    # deck.add_to_deck(pulled_card)  # Add to the deck
                elif Ten_pills_button_rect.collidepoint(event.pos):
                    # 10 pills
                    game_state = WHEN_PULLED
                    # for _ in range(10):
                        # pulled_card = gacha.pull()
                        # pulled_card_time = pygame.time.get_ticks()  # Store the current time
                        # print(f"Pulled card: {pulled_card.name} - Power: {pulled_card.power} - Rarity: {pulled_card.rarity}")
                        # deck.add_to_deck(pulled_card)  # Add to the deck

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
        mouse_pos = pygame.mouse.get_pos()
        draw_button(exit_button_rect, "Exit", exit_button_rect.collidepoint(mouse_pos))
        draw_button(pull_button_rect, "Pull", pull_button_rect.collidepoint(mouse_pos))
        draw_button(Ten_pills_button_rect, "10 Pulls", Ten_pills_button_rect.collidepoint(mouse_pos))

        # Display pulled card result for a limited time
        # if pulled_card is not None and pulled_card_time is not None:
        #     current_time = pygame.time.get_ticks()

        #     if timer(current_time, 5000, pulled_card_time):
        #         # Render text and card image
        #         text = font.render(f"You found a {pulled_card.name}", True, BLACK)
        #         screen.blit(text, (700, 50))

        #         # Scale the card image to the desired size (CARD_WIDTH, CARD_HEIGHT)
        #         resized_image = pygame.transform.scale(pulled_card.image, (200, 400))
        #         screen.blit(resized_image, (SCREEN_WIDTH // 2 - 100, 150))  # Position the resized card image

        #     else:
        #         # Reset the pulled card display
        #         pulled_card = None
        #         pulled_card_time = None

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
