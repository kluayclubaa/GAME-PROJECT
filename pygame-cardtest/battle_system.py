import random
import pygame

class battle_card:
    def __init__(self,name,power : int, path):
        self.name = name
        self.power = power
        self.path = path
        self.image = pygame.image.load(path)

class battle_storage:
    def __init__(self):
        self.storage = [
            battle_card("Gaia Theyggdrasill",100,"collection\Gaia Theyggdrasill.png"),
            battle_card("Hibaki yamanashi",100,"collection\Hibaki yamanashi.png"),
            battle_card("Hibani",100,"collection\Hibani.png"),
            battle_card("Himego Kanade",100,"collection\Himego Kanade.png"),
            battle_card("Jibril",100,"collection\Jibril.png"),
            battle_card("Kaguya Hime",100,"collection\Kaguya Hime.png"),
            battle_card("Kazuma",100,"collection\Kazuma.png"),
            battle_card("Marry Eternalblood",100,"collection\Marry Eternalblood.png"),
            battle_card("Rin shirozaki",100,"collection\Rin shirozaki.png"),
            battle_card("Shizuo Valkyria",100,"collection\Shizuo Valkyria.png"),
            battle_card("Shubaru yamato",100,"collection\Shubaru yamato.png"),
            battle_card("THE HAM",100,"collection\THE HAM.png"),
            battle_card("Traisy o' Reapper",100,"collection\Traisy o' Reapper.png"),
        ]
        self.battle_list = (random.choice(self.storage),random.choice(self.storage),random.choice(self.storage),random.choice(self.storage),random.choice(self.storage))

class Player_stat:
    def __init__(self):
        self.hp = 1000
        self.deck = []
        self.field1 = []
        self.field2 = []
        self.field3 = []
        self.field4 = []

    def add_card(self,card):
        self.deck.append(card)
        self.update_deck_positions()

    def update_deck_positions(self):
        i = 0
        for card in self.deck:
            card.position = (450 + 150 * i, 730)  # อัปเดตตำแหน่ง x ตามสูตร และตำแหน่ง y คงที่
            card.rect.topleft = card.position
            i = i + 1
class Bot_stat:
    def __init__(self):
        self.bot_hp = 1000
        self.bot_field1 = []
        self.bot_field2 = []
        self.bot_field3 = []
        self.bot_field4 = [] 