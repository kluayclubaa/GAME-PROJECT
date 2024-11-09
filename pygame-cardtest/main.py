import pygame
import random
from gacha import GachaSystem  # Import your Gacha system
import os
import sys


from battle_system import Player_stat
from battle_system import battle_storage
from battle_system import Bot_stat

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BUTTON_COLOR = (200, 0, 0)  # Red color for the buttons.


NEXT_COLOR=(200, 70, 70)
NEXTA_COLOR=(70, 150, 200)


NEXT_HOVER_COLOR = (0, 0, 255)  # Blue color

HOVER_COLOR = (100, 100, 200)
card_width = 200
card_height = 400
background_img = pygame.image.load('background/bg.png')
pull_img = pygame.image.load('background/GC.png')
gacha_background=pygame.image.load('gacha background/1.jpg')
show_rate=pygame.image.load('gacha background/background.png')
bg_col=pygame.image.load('colbg/bg.png')
deck_bg=pygame.image.load("background/deck.png")

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
next_button_rect = pygame.Rect((1550,830, 150, 30))
save_button_rect = pygame.Rect((SCREEN_WIDTH - 300, 50, 200, 100))
# Initialize systems
gacha = GachaSystem()  # Initialize the Gacha system
# Initialize the AI Battle system

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
COLLECTION2="collection2"
game_state = HOME

clock = pygame.time.Clock()
try:
    with open("deck.txt", "r") as file:
        with open("deck_replace.txt", "w") as file2:
            for line in file:
                file2.write(line)
except FileNotFoundError:
    print("Deck file not found")


# Function to draw buttons on the home page
def draw_button(rect, text, hovered=False):
    color = NEXTA_COLOR if hovered else NEXT_HOVER_COLOR
    pygame.draw.rect(screen, color, rect, border_radius=12)
    text_render = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(text_render, (rect.x + (rect.width - text_render.get_width()) // 2, rect.y + (rect.height - text_render.get_height()) // 2))



def drawnext_button(rect, text, r=False):
    color = BUTTON_COLOR
    if r:
        color = NEXT_COLOR

    
    
    pygame.draw.rect(screen, color, rect, border_radius=12)
    text_render = font_coin.render(text, True, (255, 255, 255))  # White text
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
ten_name=[]
current_card_index = 0
# Main game loop
collected_cards = []
collected_cards2=[]
deck_main={}
dragging_card = None
top_slots = [None] * 20
card_width = 80
card_height = 150
start_x = 200
start_y = 400  # Starting y position of the first row
card_spacing = 10
slots_per_row = 18
def load_collected_cards():
    global  collected_cards

    try:
        with open("collection.txt", "r") as file:
                all_cards = [line.strip() for line in file if line.strip()]
                
                collected_cards=all_cards[:10]
                
                collected_cards2=all_cards[10:]
    except FileNotFoundError:
        print("Collection file not found.")
    return collected_cards,collected_cards2



selected_card = None  # Stores currently selected card
card_offset = (0, 0)  # Offset for dragging
fixed_slots = []  # Stores fixed position slots
placed_cards = {}  # Stores cards placed in each fixed slot
deck_main = {}  # Stores initial deck from file

# Define Save button




def initialize_fixed_slots():
    """Initialize the fixed position slots (10 slots)."""
    global fixed_slots
    fixed_slot_start_x = 320  # Starting x position for the fixed slots
    fixed_slot_start_y = 50  # Starting y position for the fixed slots
    fixed_slot_start_y2 = 220
    fixed_slot_width = 120
    fixed_slot_height = 160
    fixed_slot_spacing = 10
    fixed_slots_count = 10  # Total 10 slots

    # Generate 10 fixed slots in the first row
    for i in range(fixed_slots_count):
        slot_x = fixed_slot_start_x + i * (fixed_slot_width + fixed_slot_spacing)
        slot_y = fixed_slot_start_y
        fixed_slots.append(pygame.Rect(slot_x, slot_y, fixed_slot_width, fixed_slot_height))
    # Generate 10 fixed slots in the second row
    for i in range(fixed_slots_count):
        slot_x = fixed_slot_start_x + i * (fixed_slot_width + fixed_slot_spacing)
        slot_y = fixed_slot_start_y2
        fixed_slots.append(pygame.Rect(slot_x, slot_y, fixed_slot_width, fixed_slot_height))

initialize_fixed_slots()

def update_deck_file():
    """Update deck.txt file to reflect the current deck_cards state."""
    with open("deck_replace.txt", "w") as file:
        for card_name, count in deck_main.items():
            for _ in range(count):
                file.write(card_name + "\n")
    print("Deck file updated.")

def save_fixed_slots_to_file():
    """Save the names of cards currently placed in fixed slots to deck_save.txt."""
    with open("deck_save.txt", "w") as file:
        for slot_index in sorted(placed_cards.keys()):
            card_name = placed_cards[slot_index]
            file.write(card_name + "\n")
    print("Fixed slot cards saved to deck_save.txt")
def draw_deck_page(screen, gacha, deck_cards):
    """Draw the deck page with cards arranged in the lower grid and handle card selection, dragging, and snapping."""
    global selected_card, card_offset
    card_width = 100
    card_height = 130
    deck_start_x = 300
    deck_start_y = 400  # Starting y position for the deck cards
    card_spacing = 10
    slots_per_row = 12

    # Draw deck slots in a 3-row grid (lower section)
    for row in range(3):
        for i in range(slots_per_row):
            slot_x = deck_start_x + i * (card_width + card_spacing)
            slot_y = deck_start_y + row * (card_height + card_spacing)
            slot_rect = pygame.Rect(slot_x, slot_y, card_width, card_height)
            pygame.draw.rect(screen, (255, 255, 255), slot_rect)
            pygame.draw.rect(screen, (200, 200, 200), slot_rect, 2)

    # Draw fixed slots in the upper section
    for slot_rect in fixed_slots:
        pygame.draw.rect(screen, (255, 255, 255), slot_rect)
        pygame.draw.rect(screen, (200, 200, 200), slot_rect, 2)

    # Display cards in fixed slots if placed
    for slot_index, card_name in placed_cards.items():
        for card in gacha.cards:
            if card.name == card_name:
                slot_rect = fixed_slots[slot_index]
                card_image = pygame.transform.smoothscale(card.image, (120, 160))
                screen.blit(card_image, (slot_rect.x, slot_rect.y))
                break

    # Display deck cards in the lower section and handle dragging
    card_hit_boxes = []  # List of tuples (rect, card_name)
    card_position = 0

    for card_name in list(deck_cards.keys()):  # Iterate over a copy to modify deck_cards in-place
        row = card_position // slots_per_row
        col = card_position % slots_per_row

        if row < 3:
            for card in gacha.cards:
                if card.name == card_name:
                    # Calculate initial position
                    card_x = deck_start_x + col * (card_width + card_spacing)
                    card_y = deck_start_y + row * (card_height + card_spacing)

                    # Highlight selected card for dragging
                    if selected_card == card_name:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        card_x, card_y = mouse_x - card_offset[0], mouse_y - card_offset[1]

                    # Draw card
                    card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                    card_hit_boxes.append((card_rect, card_name))
                    
                    card_image = pygame.transform.smoothscale(card.image, (card_width, card_height))
                    screen.blit(card_image, (card_x, card_y))

                    # Draw card count if > 1
                    count = deck_cards[card_name]
                    if count > 1:
                        count_font = pygame.font.Font(None, 24)
                        count_text = count_font.render(f"x{count}", True, (255, 255, 255))
                        count_rect = count_text.get_rect(bottomright=(card_x + card_width - 5, 
                                                                      card_y + card_height - 5))
                        shadow_text = count_font.render(f"x{count}", True, (0, 0, 0))
                        screen.blit(shadow_text, (count_rect.x + 1, count_rect.y + 1))
                        screen.blit(count_text, count_rect)

                    card_position += 1
                    break

    # Handle card selection, dragging, and snapping to fixed slots
    if pygame.mouse.get_pressed()[0]:  # Left click for selecting or dragging
        mouse_pos = pygame.mouse.get_pos()
        if not selected_card:
            # Start dragging if a card is clicked in the deck or fixed slots
            for card_rect, card_name in card_hit_boxes:
                if card_rect.collidepoint(mouse_pos):
                    selected_card = card_name
                    card_offset = (mouse_pos[0] - card_rect.x, mouse_pos[1] - card_rect.y)
                    break
            # Check if a card in fixed slots is clicked
            for slot_index, card_name in placed_cards.items():
                slot_rect = fixed_slots[slot_index]
                if slot_rect.collidepoint(mouse_pos):
                    selected_card = card_name
                    card_offset = (mouse_pos[0] - slot_rect.x, mouse_pos[1] - slot_rect.y)
                    # Remove the card from placed slots and add it back to deck
                    deck_cards[selected_card] = deck_cards.get(selected_card, 0) + 1
                   
                    del placed_cards[slot_index]
                    update_deck_file()  # Update file after adding card back to deck
                    break
    else:
        # On mouse release, snap to the nearest fixed slot if applicable
        if selected_card:
            mouse_pos = pygame.mouse.get_pos()
            for slot_index, slot_rect in enumerate(fixed_slots):
                if slot_rect.collidepoint(mouse_pos) and slot_index not in placed_cards:
                    # Place card in slot and update deck count
                    placed_cards[slot_index] = selected_card
                    deck_cards[selected_card] -= 1
                    
                    if deck_cards[selected_card] <= 0:
                        del deck_cards[selected_card]

                    update_deck_file()  # Update file after placing card in fixed slot

                    
                    break
      
            selected_card = None  # Deselect card after placing

    return card_hit_boxes





def load_deck():
    """Load deck from file and count unique cards."""
    global deck_main
    deck_main = {}
    try:
        with open("deck_replace.txt", "r") as file:
            for line in file:
                card_name = line.strip()
                if card_name in deck_main:
                    deck_main[card_name] += 1
                else:
                    deck_main[card_name] = 1
    except FileNotFoundError:
        print("Deck file not found")
    return deck_main




    
def draw_collection_page(screen, gacha, collected_card_names, bg_col,  page_number):
    """Draw a single page of the collection"""
    # Draw background
    screen.blit(bg_col, (150, 0))
    
    # Collection display settings
    card_width = 200
    card_height = 350
    column_x_start = 300
    row_y_start = 100
    card_spacing_x = 50
    card_spacing_y = 50
    border_thickness = 5
    inner_padding = 10
    
    # Get the cards that match the collected names
    collected_cards = [card for card in gacha.cards if card.name in collected_card_names]
    
    # Draw the cards in a grid
    for row in range(2):
        for col in range(5):
            card_x = column_x_start + col * (card_width + card_spacing_x)
            card_y = row_y_start + row * (card_height + card_spacing_y)
            
            card_index = row * 5 + col
            if card_index < len(collected_cards):
                # Draw existing card
                card = collected_cards[card_index]
                card_image = pygame.transform.scale(card.image, (card_width, card_height))
                screen.blit(card_image, (card_x, card_y))
            else:
                # Draw empty slot
                pygame.draw.rect(screen, (200, 255, 255), 
                               (card_x, card_y, card_width, card_height), 
                               border_thickness)
                pygame.draw.rect(screen, (255, 255, 255),
                               (card_x + inner_padding, 
                                card_y + inner_padding,
                                card_width - 2 * inner_padding, 
                                card_height - 2 * inner_padding))
    
    # Draw the navigation button with appropriate text
    
def check_if_card_exists(card_name, file_path):
    """Check if a card name already exists in the collection file"""
    try:
        with open(file_path, "r") as file:
            existing_cards = [line.strip() for line in file]
            return card_name in existing_cards
    except FileNotFoundError:
        return False
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
                elif pull_button_rect.collidepoint(event.pos) and coin >= pull_couse:
                    pulled_card = gacha.pull()
                    file_path = "collection.txt"
                    
                    if not check_if_card_exists(pulled_card.name, file_path):
                        with open(file_path, "a") as storage_add:
                            storage_add.write(pulled_card.name + "\n")
                    with open("deck.txt","a") as f:
                        f.write(pulled_card.name + "\n")
                    try:
                        with open("deck.txt", "r") as file:
                            with open("deck_replace.txt", "w") as file2:
                                for line in file:
                                    file2.write(line)
                    except FileNotFoundError:
                        print("Deck file not found")

                    
                    game_state = SHOW_STATE
                    coin -= 100
                        
                elif Ten_pills_button_rect.collidepoint(event.pos) and coin >= ten_pull_couse:
                    tenshow.clear()  # Clear previous pulls
                    for i in range(10):
                        pulled_card = gacha.pull()
                        tenshow.append(pulled_card.show)
                        
                        file_path = "collection.txt"
                        if not check_if_card_exists(pulled_card.name, file_path):
                            with open(file_path, "a") as storage_add:
                                storage_add.write(pulled_card.name + "\n")
                        with open("deck.txt","a") as f:
                            f.write(pulled_card.name + "\n")
                        try:
                            with open("deck.txt", "r") as file:
                                with open("deck_replace.txt", "w") as file2:
                                    for line in file:
                                        file2.write(line)
                        except FileNotFoundError:
                            print("Deck file not found")
                    
                    game_state = SHOWTEN_STATE
                    coin -= 1000
                    current_card_index = 0  # Reset card index for new pulls
                    
            elif game_state == WHEN_PULLED:
                if exit_button_rect.collidepoint(event.pos):
                    game_state = GACHA
                elif plus_button_rect.collidepoint(event.pos):
                    code_active = True
                elif pull_button_rect.collidepoint(event.pos) and coin >= pull_couse:
                    pulled_card = gacha.pull()
                    file_path = "collection.txt"
                    
                    if not check_if_card_exists(pulled_card.name, file_path):
                        with open(file_path, "a") as storage_add:
                            storage_add.write(pulled_card.name + "\n")
                    with open("deck.txt","a") as f:
                        f.write(pulled_card.name + "\n")
                    try:
                        with open("deck.txt", "r") as file:
                            with open("deck_replace.txt", "w") as file2:
                                for line in file:
                                    file2.write(line)
                    except FileNotFoundError:
                        print("Deck file not found")
                    game_state = SHOW_STATE
                    coin -= 100
                        
                elif Ten_pills_button_rect.collidepoint(event.pos) and coin >= ten_pull_couse:
                    tenshow.clear()  # Clear previous pulls
                    for i in range(10):
                        pulled_card = gacha.pull()
                        tenshow.append(pulled_card.show)
                        
                        file_path = "collection.txt"
                        if not check_if_card_exists(pulled_card.name, file_path):
                            with open(file_path, "a") as storage_add:
                                storage_add.write(pulled_card.name + "\n")
                        with open("deck.txt","a") as f:
                            f.write(pulled_card.name + "\n")
                        try:
                            with open("deck.txt", "r") as file:
                                with open("deck_replace.txt", "w") as file2:
                                    for line in file:
                                        file2.write(line)
                        except FileNotFoundError:
                            print("Deck file not found")
                    
                    game_state = SHOWTEN_STATE
                    coin -= 1000
                    current_card_index = 0  # Reset card index for new pulls
            
            elif game_state == SHOWTEN_STATE:
                if event.button == 1:
                    current_card_index += 1
                    if current_card_index >= len(tenshow):
                        game_state = WHEN_PULLED
            elif game_state == SHOW_STATE:
                if event.button == 1:
                    game_state = WHEN_PULLED
            elif game_state == COLLECTION:
                if next_button_rect.collidepoint(event.pos):
                    game_state = COLLECTION2
            elif game_state == COLLECTION2:
                if next_button_rect.collidepoint(event.pos):
                    game_state = COLLECTION
            elif game_state == DECK:
                if save_button_rect.collidepoint(event.pos):
                    save_fixed_slots_to_file()
               
                
            

        coin = handle_code_entry(event, coin)

    # Display home screen
    if game_state == HOME:
        screen.blit(background_img, (150, 0))
        

        mouse_pos = pygame.mouse.get_pos()
        draw_button(battle_button_rect, "Battle", battle_button_rect.collidepoint(mouse_pos))
        draw_button(deck_button_rect, "Deck", deck_button_rect.collidepoint(mouse_pos))
        draw_button(gacha_button_rect, "Gacha", gacha_button_rect.collidepoint(mouse_pos))
        draw_button(collection_button_rect, "Collection", collection_button_rect.collidepoint(mouse_pos))

    elif game_state == BATTLE:
        battle_map = pygame.image.load("background/battle.jpg")
        battle_map = pygame.transform.scale(battle_map, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(battle_map, (0, 0))

        def location_click_card(mouse_x,mouse_y):
            if 450 <= mouse_x <= 570 and 730 <= mouse_y <= 890:
                return 0
            elif 600 <= mouse_x <= 720 and 730 <= mouse_y <= 890:
                return 1
            elif 750 <= mouse_x <= 870 and 730 <= mouse_y <= 890:
                return 2
            elif 900 <= mouse_x <= 1020 and 730 <= mouse_y <= 890:
                return 3
            elif 1050 <= mouse_x <= 1170 and 730 <= mouse_y <= 890:
                return 4
            elif 1200 <= mouse_x <= 1320 and 730 <= mouse_y <= 890:
                return 5
            elif 1350 <= mouse_x <= 1470 and 730 <= mouse_y <= 890:
                return 6
        
        class Picture:
            def __init__(self, position, image,power):
                self.image = image
                self.rect = self.image.get_rect(topleft=position)
                self.position = position
                self.target_position = [(480, 502),(767, 502),(1052, 502),(1342, 502)]  
                self.start_position = position  
                self.dragging = False  
                self.placed = False
                self.power = power

            def draw(self, screen):
                screen.blit(self.image, self.rect.topleft)

            def check_click(self, mouse_position):
                if self.rect.collidepoint(mouse_position):
                    return True
    
            def start_drag(self):
                if not self.placed:
                    self.dragging = True
    
            def stop_drag(self):
                self.dragging = False
                i = 0
                for target_position in self.target_position:
                    distance_to_target = pygame.math.Vector2(self.position[0] - target_position[0], self.position[1] - target_position[1]).length()
                    if distance_to_target <= 100:
                        self.position = target_position
                        self.rect.topleft = self.position  # อัพเดตตำแหน่งจริงใน rect
                        self.image = pygame.transform.smoothscale(self.image, (90,120))
                        self.placed = True
                        if i == 0:
                            player1.field1.append(player1.deck[location_click])
                        elif i == 1:
                            player1.field2.append(player1.deck[location_click])
                        elif i == 2:
                            player1.field3.append(player1.deck[location_click])
                        elif i == 3:
                            player1.field4.append(player1.deck[location_click])
                        player1.deck.remove(player1.deck[location_click])
                        player1.update_deck_positions()
                        break
                    i += 1
                else:
               
                    self.position = self.start_position
                    self.rect.topleft = self.position

            def update(self, mouse_pos):
                if self.dragging:
                    # หากลากภาพ, อัพเดตตำแหน่ง
                    self.position = mouse_pos
                    self.rect.topleft = self.position
        battle_bot = Bot_stat()
        player1 = Player_stat()
        new_width, new_height = 120, 160
#มาแก้ทีหลังให้เอาชื่อจากdeck
        my_battle_storage = battle_storage()
        i = 0
        for card in my_battle_storage.battle_list:
            mycard = card.image
            mycard = pygame.transform.smoothscale(mycard,(new_width,new_height))
            image = Picture((450 + 150*i,730),mycard,card.power)
            player1.add_card(image)
            i += 1
        
        location_click = None
        for round in range(10):
            print("round",round+1)
            continue_play = True
            while continue_play:
                battle_map = pygame.image.load("background/battle_map.jpg")
                battle_map = pygame.transform.scale(battle_map, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(battle_map, (0, 0))

                if player1.deck:
                    for card in player1.deck:  
                        card.draw(screen)
                if player1.field1:  
                    for card in player1.field1:  
                        card.draw(screen)

                if player1.field2:  
                    for card in player1.field2:  
                        card.draw(screen)
                
                if player1.field3:  
                    for card in player1.field3:  
                        card.draw(screen)
                
                if player1.field4:  
                    for card in player1.field4:  
                        card.draw(screen)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # K_RETURN คือปุ่ม Enter
                            continue_play = not continue_play

                    if event.type == pygame.MOUSEBUTTONDOWN: # ตรวจจับการคลิกเมาส์
                        mouse_pos = pygame.mouse.get_pos()
                        x_pos, y_pos = mouse_pos
                        location_click = location_click_card(x_pos, y_pos)  
                        if location_click is not None and location_click < len(player1.deck):  # ตรวจสอบว่า location_click ถูกต้อง
                            if player1.deck[location_click].check_click(mouse_pos):
                                player1.deck[location_click].start_drag()  # เริ่มลากภาพ

                    elif event.type == pygame.MOUSEBUTTONUP and location_click is not None:
                        if location_click < len(player1.deck):
                            player1.deck[location_click].stop_drag()
                        location_click = None
            
                # อัพเดตตำแหน่งของภาพ
                mouse_pos = pygame.mouse.get_pos()
                if location_click is not None and location_click < len(player1.deck):
                    player1.deck[location_click].update(mouse_pos)
                pygame.display.flip()
            #ทำระบบเล่นฝั่งbot
            num = 0
            if battle_bot.bot_field1 == []:
                num += 1
            if battle_bot.bot_field2 == []:
                num += 1
            if battle_bot.bot_field3 == []:
                num += 1
            if battle_bot.bot_field4 == []:
                num += 1
            random_add_card_num_bot = random.randint(1,num)
            if random_add_card_num_bot == 1:
                random_add_card_num_bot = random.randint(1,num)
                for i in range(random_add_card_num_bot):
                    if battle_bot.bot_field1 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((480,285),random_card_image,random_card.power)
                        battle_bot.bot_field1.append(random_card)

                    elif battle_bot.bot_field2 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((767,285),random_card_image,random_card.power)
                        battle_bot.bot_field2.append(random_card)

                    elif battle_bot.bot_field3 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1052,285),random_card_image,random_card.power)
                        battle_bot.bot_field3.append(random_card)

                    elif battle_bot.bot_field4 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1342,285),random_card_image,random_card.power)
                        battle_bot.bot_field4.append(random_card)

            elif random_add_card_num_bot == 2:
                random_add_card_num_bot = random.randint(1,num)
                for i in range(random_add_card_num_bot):
                    if battle_bot.bot_field4 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1342,285),random_card_image,random_card.power)
                        battle_bot.bot_field4.append(random_card)

                    elif battle_bot.bot_field3 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1052,285),random_card_image,random_card.power)
                        battle_bot.bot_field3.append(random_card)

                    elif battle_bot.bot_field2 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((767,285),random_card_image,random_card.power)
                        battle_bot.bot_field2.append(random_card)

                    elif battle_bot.bot_field1 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((480,285),random_card_image,random_card.power)
                        battle_bot.bot_field1.append(random_card)

            elif random_add_card_num_bot == 3:
                random_add_card_num_bot = random.randint(1,num)
                for i in range(random_add_card_num_bot):
                    if battle_bot.bot_field1 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((480,285),random_card_image,random_card.power)
                        battle_bot.bot_field1.append(random_card)

                    elif battle_bot.bot_field3 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1052,285),random_card_image,random_card.power)
                        battle_bot.bot_field3.append(random_card)

                    elif battle_bot.bot_field2 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((767,285),random_card_image,random_card.power)
                        battle_bot.bot_field2.append(random_card)

                    elif battle_bot.bot_field4 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1342,285),random_card_image,random_card.power)
                        battle_bot.bot_field4.append(random_card)

            elif random_add_card_num_bot == 4:
                random_add_card_num_bot = random.randint(1,num)
                for i in range(random_add_card_num_bot):
                    if battle_bot.bot_field4 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1342,285),random_card_image,random_card.power)
                        battle_bot.bot_field4.append(random_card)

                    elif battle_bot.bot_field2 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((767,285),random_card_image,random_card.power)
                        battle_bot.bot_field2.append(random_card)

                    elif battle_bot.bot_field3 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((1052,285),random_card_image,random_card.power)
                        battle_bot.bot_field3.append(random_card)

                    elif battle_bot.bot_field1 == []:
                        random_card = random.choice(my_battle_storage.storage)
                        random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                        random_card = Picture((480,285),random_card_image,random_card.power)
                        battle_bot.bot_field1.append(random_card)


            continue_play_bot = True    
            while continue_play_bot:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # K_RETURN คือปุ่ม Enter
                            continue_play_bot = not continue_play_bot


            if player1.hp <= 0:
                print("lose")


            if len(player1.deck) < 7:
                random_card = random.choice(my_battle_storage.storage)
                random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                loca_add = len(player1.deck) - 1
                random_card = Picture((450 + 150*loca_add,730),random_card_image,random_card.power)
                player1.add_card(random_card)
            else:
                print("your deck is full")
            
            
            


            






    elif game_state == DECK:
    # แสดงพื้นหลัง
        mouse_pos = pygame.mouse.get_pos()
        deck_bg = pygame.transform.scale(deck_bg, (SCREEN_WIDTH-150, SCREEN_HEIGHT))
        rect = deck_bg.get_rect()
        rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(deck_bg, rect)
        draw_button(save_button_rect, "Save", save_button_rect.collidepoint(mouse_pos))
    
    # โหลดและแสดงการ์ดในเด็ค
        deck_main = load_deck()
        draw_deck_page(screen, gacha, deck_main)
    
    # ถ้ามีการ์ดที่ถูกเลือก ให้แสดงภาพพรีวิว
        
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            game_state = HOME
            selected_card = None

    elif game_state == GACHA:
        screen.blit(pull_img, (150, 0))


        
       
        



        show_rate_scaled = pygame.transform.scale(show_rate, (SCREEN_WIDTH-500, SCREEN_HEIGHT-200))
        show_rate_rect = show_rate_scaled.get_rect(center=(SCREEN_WIDTH//2, 390))
        
        screen.blit(show_rate_scaled, show_rate_rect)
 



       
        
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
        mouse_pos = pygame.mouse.get_pos()

        collected_cards_page1, collected_cards_page2 = load_collected_cards()
        draw_collection_page(screen, gacha, collected_cards_page1, bg_col, 
                        1)
        drawnext_button(next_button_rect, "next", next_button_rect.collidepoint(mouse_pos))
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
             game_state = HOME
    elif game_state == COLLECTION2:
        mouse_pos = pygame.mouse.get_pos()

        collected_cards_page1, collected_cards_page2 = load_collected_cards()
        draw_collection_page(screen, gacha, collected_cards_page2, bg_col, 
                         2)
        drawnext_button(next_button_rect, "previous", next_button_rect.collidepoint(mouse_pos))
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
