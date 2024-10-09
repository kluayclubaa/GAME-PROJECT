class Collection:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def display_collection(self):
        """For demo purposes, print the card names."""
        for card in self.cards:
            print(f"{card.name} (Power: {card.power}, Rarity: {card.rarity})")
