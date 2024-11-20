import pygame
import random
from gacha import GachaSystem  # Import your Gacha system
import os
import sys
from deck import DeckManager

from battle_system import Player_stat
from battle_system import battle_storage
from battle_system import Bot_stat
from battle_system import Process_battle
from battle_system import Picture
from button import Button


# Initialize pygame
pygame.init()
pygame.mixer.init()
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
pygame.mixer.music.load("music/hopes.mp3")


# Load the coin image
coin_img = pygame.image.load('asset/coin.png')  # Path to your coin image
coin_img = pygame.transform.scale(coin_img, (30, 30))  # Resize the coin image if necessary

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Card Game Home Page")

font = pygame.font.Font(pygame.font.match_font('impact'), 60)
font_coin=pygame.font.Font(pygame.font.match_font('MN Pu Khem'),32)
font_coin1=pygame.font.Font(pygame.font.match_font('MN Pu Khem'),128)


# Button setup
button_width, button_height = 400, 50


exit_button_rect = pygame.Rect((1300, 800, button_width, button_height))
pull_button_rect = pygame.Rect((200, 800, button_width, button_height))
Ten_pills_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, 800, button_width, button_height))
next_button_rect = pygame.Rect((1550,830, 150, 30))
save_button_rect = pygame.Rect((SCREEN_WIDTH - 300, 50, 200, 100))
playButton = Button(600, 300, "button/PlayHover.png", "button/Play.png", 250, 150)
DeckButton=Button(1000,300,"button/DeckHover.png","button/Deck.png",250,150)
GachaButton=Button(600,600,"button/GachaHover.png","button/Gacha.png",250,150)
CollectionButton=Button(1000,600,"button/CollectionHover.png","button/Collection.png",250,150)

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
if game_state == HOME:
    pygame.mixer.music.play()
clock = pygame.time.Clock()
try:
    with open("deck.txt", "r") as file:
        with open("deck_replace.txt", "w") as file2:
            for line in file:
                file2.write(line)
except FileNotFoundError:
    print("Deck file not found")

def end_game_screen(screen, message, game_state):
    screen.fill((255,255,255))
    display_text(screen, message, 100, (0, 0, 0), (960, 350))
    display_text(screen, "Press Enter to return to the main screen.", 100, (0, 0, 0), (960, 450))
    pygame.display.flip()
    end = True
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # K_RETURN คือปุ่ม Enter
                    end = False
                    return game_state
def display_text(screen, text, font_size, color, position):
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        screen.blit(text_surface, text_rect)

def render_battle_screen(screen, player1, battle_bot, round, screen_width, screen_height):
    battle_map = pygame.image.load("background/battle_map.jpg")
    battle_map = pygame.transform.scale(battle_map, (screen_width, screen_height))
    screen.blit(battle_map, (0, 0))
    
    display_text(screen, f" {player1.hp} / 3000", 50, (255, 255, 255), (170, 450))
    display_text(screen, f"{battle_bot.bot_hp} / 3000", 50, (255, 255, 255), (1750, 450))
    display_text(screen, f"Round {round}", 100, (255, 255, 255), (960, 450))
    
    all_fields = [player1.deck, player1.field1, player1.field2, player1.field3, player1.field4,battle_bot.bot_field1, battle_bot.bot_field2, battle_bot.bot_field3, battle_bot.bot_field4]
    
    for field in all_fields:
        if field:
            for card in field:
                card.draw(screen)
    
    # แสดงการ์ดใน tome ของ player1 และ battle_bot
    if player1.tome:
        player_tome_image = pygame.transform.smoothscale(player1.tome[-1].image, (156, 208))
        screen.blit(player_tome_image, (128, 641))
    if battle_bot.tome:
        bot_tome_image = pygame.transform.smoothscale(battle_bot.tome[-1].image, (156, 208))
        screen.blit(bot_tome_image, (128, 49))

def check_use_magic_card(all_list):
    card_type = None
    card_location = None
    for num,card in enumerate(all_list):
        if card != []:
            if card[0].power == 8888:
                card_type = "heal"
                card_location = num
            elif card[0].power == 9999:
                card_type = "clear"
                card_location = num
    if card_type != None and card_location != None:
        return [card_type,all_list[card_location]]
    return [None,None]

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
def draw_stylized_text(text, font, main_color, shadow_color, pos, shadow_offset=(4, 4)):
    # Render the shadow text first
    shadow_text = font.render(text, True, shadow_color)
    screen.blit(shadow_text, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
    
    # Render the main text on top
    main_text = font.render(text, True, main_color)
    screen.blit(main_text, pos)
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


import pygame


    
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
deck_manager = DeckManager()

 
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
            if save_button_rect.collidepoint(event.pos):
                    deck_manager.save_fixed_slots_to_file()
            if game_state == HOME:
                
                if playButton.is_clicked(event):
                    game_state = BATTLE
                elif DeckButton.is_clicked(event):
                    game_state = DECK
                elif GachaButton.is_clicked(event):
                     game_state = GACHA
                elif CollectionButton.is_clicked(event):
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
                    
            # elif game_state == WHEN_PULLED:
            #     if exit_button_rect.collidepoint(event.pos):
            #         game_state = GACHA
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
                        game_state = GACHA
            elif game_state == SHOW_STATE:
                if event.button == 1:
                    game_state = GACHA
            elif game_state == COLLECTION:
                if next_button_rect.collidepoint(event.pos):
                    game_state = COLLECTION2
            elif game_state == COLLECTION2:
                if next_button_rect.collidepoint(event.pos):
                    game_state = COLLECTION
            
               
                
            

        coin = handle_code_entry(event, coin)

    # Display home screen
    if game_state == HOME:
        screen.blit(background_img, (0, 0))
        
        

        main_color=(255, 215, 0)
       
        

        drop_color=(0, 0, 0)
       
        mouse_pos = pygame.mouse.get_pos()
        playButton.draw(screen)
        DeckButton.draw(screen)
        GachaButton.draw(screen)
        CollectionButton.draw(screen)



        



    elif game_state == BATTLE:
        battle_map = pygame.image.load("background/battle.jpg")
        battle_map = pygame.transform.scale(battle_map, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(battle_map, (10, 0))


       


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
    
            def stop_drag(self,player):
                player1 = player
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
                        player1.continue_play = not player1.continue_play
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
        bot_battle_storage = battle_storage()
        deck_sto = open("deck_save.txt","r")
        
        for card in deck_sto:
            card = card.strip()
            for i in my_battle_storage.storage:
                if card == i.name:
                    my_battle_storage.deck_storage.append(i)
        for i in range(5):
            mycard = random.choice(my_battle_storage.deck_storage)
            my_battle_storage.deck_storage.remove(mycard)
            mycard_im = pygame.transform.smoothscale(mycard.image,(new_width,new_height))
            image = Picture((450 + 150*i,730),mycard_im,mycard.power)
            player1.add_card(image)
        
        location_click = None
        round = 1
        check_end = True
        while round <= 10 and check_end:
            
            player1.continue_play = True
            while player1.continue_play:
                render_battle_screen(screen, player1, battle_bot, round, SCREEN_WIDTH, SCREEN_HEIGHT)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                   player1.hp=0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:  # K_RETURN คือปุ่ม Enter
                            player1.continue_play = not player1.continue_play

                    if event.type == pygame.MOUSEBUTTONDOWN: # ตรวจจับการคลิกเมาส์
                        mouse_pos = pygame.mouse.get_pos()
                        x_pos, y_pos = mouse_pos
                        location_click = location_click_card(x_pos, y_pos)  
                        if location_click is not None and location_click < len(player1.deck):  # ตรวจสอบว่า location_click ถูกต้อง
                            if player1.deck[location_click].check_click(mouse_pos):
                                player1.deck[location_click].start_drag()  # เริ่มลากภาพ

                    elif event.type == pygame.MOUSEBUTTONUP and location_click is not None:
                        if location_click < len(player1.deck):
                            player1.deck[location_click].stop_drag(player1)
                        location_click = None
            
                # อัพเดตตำแหน่งของภาพ
                mouse_pos = pygame.mouse.get_pos()
                if location_click is not None and location_click < len(player1.deck):
                    player1.deck[location_click].update(mouse_pos)
                pygame.display.flip()
            render_battle_screen(screen, player1, battle_bot, round, SCREEN_WIDTH, SCREEN_HEIGHT)
            
            #ทำระบบเล่นฝั่งbot
            def add_card_to_field(field, position, storage):
                if field == []:
                    random_card = random.choice(storage)
                    random_card_image = pygame.transform.smoothscale(random_card.image, (90, 120))
                    random_card = Picture(position, random_card_image, random_card.power)
                    field.append(random_card)

            
                    
            if battle_bot.bot_field1 == []:
                add_card_to_field(battle_bot.bot_field1, (480, 285), bot_battle_storage.storage)
            elif battle_bot.bot_field2 == []:
                add_card_to_field(battle_bot.bot_field2, (767, 285), bot_battle_storage.storage)
            elif battle_bot.bot_field3 == []:
                add_card_to_field(battle_bot.bot_field3, (1052, 285), bot_battle_storage.storage)
            elif battle_bot.bot_field4 == []:
                add_card_to_field(battle_bot.bot_field4, (1342, 285), bot_battle_storage.storage)
            #ระบบเลือกการ์ดตีของฝั่งผู้เล่น
            my_process_battle = Process_battle()
            continue_play_select_card = True
            deck_select_card = []
            bot_select_card = []  
            def blink_color():
                color = [(255, 0, 0), (0, 255, 0)]
                blink = 0
                blink_time = 0
                current_time = pygame.time.get_ticks()
                if current_time - blink_time > 500:
                    blink_time = current_time
                    blink = (blink + 1) % 2
                return color[blink]
            RED = blink_color()
            

            all_player_field = [player1.field1, player1.field2, player1.field3, player1.field4]
            all_bot_field = [battle_bot.bot_field1, battle_bot.bot_field2, battle_bot.bot_field3, battle_bot.bot_field4]
            
            use_magic_card = check_use_magic_card(all_player_field)
            if use_magic_card[0] == "clear":
                battle_bot.bot_field1,battle_bot.bot_field2,battle_bot.bot_field3,battle_bot.bot_field4 = [],[],[],[]
                use_magic_card[1] = [] 
            elif use_magic_card[0] == "heal":
                player1.hp += 500
                use_magic_card[1] = [] 
            else:
                #วนการ์ดที่จะใช้โจมตีของฝั่งผู้เล่นจนครบทุกใบ
                for num,the_field in enumerate(all_player_field):
                    P_rect_x, P_rect_y, P_rect_width, P_rect_height = None, None, 100, 130
                    B_rect_x, B_rect_y, B_rect_width, B_rect_height = None, None, 100, 130
                    continue_play_select_card = True
                    if battle_bot.bot_field1 == [] and battle_bot.bot_field2 == [] and battle_bot.bot_field3 == [] and battle_bot.bot_field4 == [] and the_field != []:
                        battle_bot.bot_hp -= the_field[0].power
                    else:
                        while continue_play_select_card and the_field != []:
                            P_rect_x,P_rect_y = player1.check_rect(num)
                            deck_select_card = the_field
                            render_battle_screen(screen, player1, battle_bot, round, SCREEN_WIDTH, SCREEN_HEIGHT)
                            if P_rect_x and P_rect_y and the_field != []:
                                pygame.draw.rect(screen, RED, (P_rect_x, P_rect_y, P_rect_width, P_rect_height), 5)
                            if B_rect_x and B_rect_y:
                                pygame.draw.rect(screen, RED, (B_rect_x, B_rect_y, B_rect_width, B_rect_height), 5)
                            pygame.display.flip()       
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = pygame.mouse.get_pos()
                                    x_pos, y_pos = mouse_pos
                
                                    bot_select_card = battle_bot.check_got_click(x_pos,y_pos,the_field)
                                    B_rect_x, B_rect_y = battle_bot.check_got_click_frame(x_pos,y_pos,bot_select_card)

                                    

                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:  # K_RETURN คือปุ่ม Enter
                                        continue_play_select_card = not continue_play_select_card
                    

                    
                    # คำนวนเลือด
                    if deck_select_card != [] and bot_select_card != []:
                        player1.hp, battle_bot.bot_hp = my_process_battle.process_battle_P_B(deck_select_card, bot_select_card, player1.hp, battle_bot.bot_hp, player1.tome, battle_bot.tome)
                
            
            
            #ระะบบbot ตี player
            all_player_field = [player1.field1, player1.field2, player1.field3, player1.field4,]
            all_bot_field = [battle_bot.bot_field1, battle_bot.bot_field2, battle_bot.bot_field3, battle_bot.bot_field4]
            bot_attacker = []
            player_defender = []
            use_magic_card = check_use_magic_card(all_bot_field)
            if use_magic_card[0] == "clear":
                player1.field1, player1.field2, player1.field3, player1.field4 = [],[],[],[]
                use_magic_card[1] = [] 
            elif use_magic_card[0] == "heal":
                battle_bot.bot_hp += 500
                use_magic_card[1] = [] 
            else:
                for num,bot_attacker in enumerate(all_bot_field):
                    if bot_attacker != []:
                        if player1.field1 == [] and player1.field2 == [] and player1.field3 == [] and player1.field4 == []:
                            player1.hp -= bot_attacker[0].power
                        else:
                            player_defender = []
                            for num,the_defender in enumerate(all_player_field):
                                if the_defender != []:
                                    if player_defender == [] and the_defender[0].power <= bot_attacker[0].power:
                                        player_defender = the_defender
                                    if player_defender != []:
                                        if player_defender[0].power < the_defender[0].power < bot_attacker[0].power:
                                            player_defender = the_defender
                            if player_defender != []:
                                P_rect_x, P_rect_y, P_rect_width, P_rect_height = None, None, 100, 130
                                B_rect_x, B_rect_y, B_rect_width, B_rect_height = None, None, 100, 130

                                
                                if bot_attacker == battle_bot.bot_field1:
                                    B_rect_x, B_rect_y = (475,280)
                                elif bot_attacker == battle_bot.bot_field2:
                                    B_rect_x, B_rect_y = (762,280)
                                elif bot_attacker == battle_bot.bot_field3:
                                    B_rect_x, B_rect_y = (1047,280)
                                elif bot_attacker == battle_bot.bot_field4:
                                    B_rect_x, B_rect_y = (1337,280)

                                if player_defender == player1.field1:
                                    P_rect_x, P_rect_y = (475,497)
                                elif player_defender == player1.field2:
                                    P_rect_x, P_rect_y = (762,497)
                                elif player_defender == player1.field3:
                                    P_rect_x, P_rect_y = (1047,497)
                                elif player_defender == player1.field4:
                                    P_rect_x, P_rect_y = (1337,497)
                                
                                next_turn = True
                                while next_turn:
                                    BLUE = (0,0,255)
                                    pygame.draw.rect(screen, BLUE, (P_rect_x, P_rect_y, P_rect_width, P_rect_height), 5)
                                    pygame.draw.rect(screen, BLUE, (B_rect_x, B_rect_y, B_rect_width, B_rect_height), 5)
                                    pygame.display.flip()
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_RETURN:  # K_RETURN คือปุ่ม Enter
                                                next_turn = False
                                player1.hp, battle_bot.bot_hp = my_process_battle.process_battle_B_P(player_defender, bot_attacker, player1.hp, battle_bot.bot_hp, player1.tome, battle_bot.tome)
            keys = pygame.key.get_pressed()   
            # การเช็คเงื่อนไขการจบเกม
            if player1.hp <= 0 and battle_bot.bot_hp <= 0:
                game_state = end_game_screen(screen, "Draw", HOME)
                check_end = False
            elif player1.hp <= 0:
                game_state = end_game_screen(screen, "Lose", HOME)
                check_end = False
            elif battle_bot.bot_hp <= 0:
                game_state = end_game_screen(screen, "Win", HOME)
                check_end = False
            elif player1.hp >= 0 and battle_bot.bot_hp >= 0 and round == 9:
                game_state = end_game_screen(screen, "Draw", HOME)
                check_end = False
            

            


            if len(player1.deck) < 7:
                if my_battle_storage.deck_storage:
                    random_card = random.choice(my_battle_storage.deck_storage)
                    my_battle_storage.deck_storage.remove(random_card)
                    random_card_image = pygame.transform.smoothscale(random_card.image,(new_width,new_height))
                    loca_add = len(player1.deck) - 1
                    random_card = Picture((450 + 150*loca_add,730),random_card_image,random_card.power)
                    player1.add_card(random_card)
                    
            else:
                print("your deck is full")
            round += 1
        

            
            
            


            






    elif game_state == DECK:
    # แสดงพื้นหลัง
        mouse_pos = pygame.mouse.get_pos()
        deck_bg = pygame.transform.scale(deck_bg, (SCREEN_WIDTH-150, SCREEN_HEIGHT))
        rect = deck_bg.get_rect()
        rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(deck_bg, rect)
        draw_button(save_button_rect, "Save", save_button_rect.collidepoint(mouse_pos))
    
    # โหลดและแสดงการ์ดในเด็ค
        deck_cards = deck_manager.load_deck()  
        deck_manager.draw_deck_page(screen, gacha, deck_cards)
    
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
            

    elif game_state == SHOW_STATE:
        resize_show_card=pygame.transform.scale(pulled_card.show,(1550,900))
        
        screen.blit(resize_show_card, (180, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            game_state = GACHA
    elif game_state == SHOWTEN_STATE:
       
        if tenshow:
            resize_show_card=pygame.transform.scale(tenshow[current_card_index],(1550,900))
        
            screen.blit(resize_show_card, (180, 0))
          

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            game_state = GACHA


    
        

    pygame.display.update()
    clock.tick(30)



pygame.quit()
