import random
from gacha import GachaSystem
class player_control:

    def __init__(self, hp: int, cost: int):
        self.hp = hp
        self.cost = cost
        self.deck = []
        self.field = []

    def update_stat(self, hp_left: int, round: int):
        self.hp = hp_left
        self.cost = round + 2

    def add_card(self):
        name_from_gachasystem = GachaSystem()
        card_name = name_from_gachasystem.get_card_names()
        random_name = random.choice(card_name)
        self.deck.append(random_name)

    def sent_card(self,selected_card):
        self.field.append(selected_card)
        self.deck.remove(selected_card)