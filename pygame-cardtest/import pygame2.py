import pygame
import random

# กำหนดขนาดหน้าจอ
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 900

# สร้างคลาส Card
class Card:
    def __init__(self, name, power, rarity, image_path, couse, number, show_path):
        """Initialize card with name, power, rarity, and an image."""
        self.name = name
        self.power = power  # Power as integer
        self.rarity = rarity
        self.image = pygame.image.load(image_path)  # Load card image
        self.couse = couse
        self.number = number
        self.show = pygame.image.load(show_path)

# สร้างคลาส GachaSystem
class GachaSystem:
    def __init__(self):
        # Define some cards with different rarities, powers, and images
        self.cards = [
            Card("Kazuma", 3, "Common", "collection/Kazuma.png", 1, 1, "showcaracter/Kazuma.png"),
            Card("Shubaru yamato", 5, "Rare", "collection/Shubaru yamato.png", 2, 2, "showcaracter/Shubaru yamato.png"),
            Card("Rin shirozaki", 5, "Rare", "collection/Rin shirozaki.png", 2, 3, "showcaracter/Rin shirozaki.png"),
            # ... Add other cards here ...
        ]

    def get_card(self):
        return self.cards

# สร้างคลาส player_control
class player_control:
    def __init__(self, hp: int, cost: int):
        self.hp = hp
        self.cost = cost
        self.deck = []
        self.field = []
        self.tome = []

    def update_stat(self, hp_left: int, round: int):
        self.hp = hp_left
        self.cost = round + 2

    def add_card(self):
        info_from_gachasystem = GachaSystem()
        card_info = info_from_gachasystem.get_card()
        random_card = random.choice(card_info)
        self.deck.append(random_card)

    def sent_card(self, location_of_selected_card: int):
        self.field.append(self.deck[location_of_selected_card])
        self.deck.pop(location_of_selected_card)

    def deck_to_tome(self, location_of_selected_card: int):
        self.tome.append(self.deck[location_of_selected_card])
        self.deck.pop(location_of_selected_card)

    def field_to_tome(self, location_of_selected_card: int):
        self.tome += self.field
        self.field = []

    def draw_deck_card(self, screen):
        # วาดการ์ดทั้งหมดใน deck
        x_offset = 450 # ตำแหน่งเริ่มต้นในการวาดการ์ด
        y_offset = 730  # ตำแหน่งเริ่มต้นบนหน้าจอ (เอาไว้ด้านล่าง)

        for card in self.deck:
            # วาดการ์ดแต่ละใบ
            card.image = pygame.transform.smoothscale(card.image, (120,160))
            screen.blit(card.image, (x_offset, y_offset))
            x_offset += 150  # ย้ายไปขวาเพื่อวาดการ์ดถัดไป (เพิ่มความห่างระหว่างการ์ด)

# ฟังก์ชันหลัก
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gacha Game")

    # สร้าง player
    player = player_control(hp=20, cost=3)

    # เพิ่มการ์ดให้กับ player
    for _ in range(5):  # เพิ่มการ์ด 5 ใบ
        player.add_card()

    while True:
        battle_map = pygame.image.load("C:/Users/Punn/Downloads/battle_map.jpg")
        battle_map = pygame.transform.scale(battle_map, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(battle_map, (0, 0))

        # วาดการ์ดจาก deck
        player.draw_deck_card(screen)

        # ตรวจสอบเหตุการณ์ต่างๆ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.flip()

# รันโปรแกรมหลัก
main()
