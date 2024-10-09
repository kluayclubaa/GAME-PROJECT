import random

class AIBattle:
    def __init__(self):
        self.ai_deck = [self.generate_random_card() for _ in range(5)]

    def generate_random_card(self):
        """Generate a simple AI card with random power."""
        return random.randint(1, 10)

    def battle(self, player_deck):
        player_hp = 5
        ai_hp = 5

        for i in range(5):
            player_card_power = player_deck[i].power
            ai_card_power = self.ai_deck[i]

            if player_card_power > ai_card_power:
                ai_hp -= 1
            elif player_card_power < ai_card_power:
                player_hp -= 1

            if player_hp == 0 or ai_hp == 0:
                break

        if player_hp > ai_hp:
            return "Player Wins!"
        elif ai_hp > player_hp:
            return "AI Wins!"
        else:
            return "Draw!"
