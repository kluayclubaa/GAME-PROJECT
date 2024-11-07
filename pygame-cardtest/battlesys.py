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
        info_from_gachasystem = GachaSystem()
        card_info = info_from_gachasystem.get_card()
        random_card = random.choice(card_info)
        self.deck.append(random_card)

    def sent_card(self,location_of_selected_card: int):
        self.field.append(self.deck[location_of_selected_card])
        self.deck.pop(location_of_selected_card)