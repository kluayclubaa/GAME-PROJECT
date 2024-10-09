class Deck:
    def __init__(self, collection):
        self.collection = collection
        self.deck = []

    def add_to_deck(self, card):
        if card in self.collection.cards:
            self.deck.append(card)

    def show_deck(self):
        for card in self.deck:
            print(f"{card.name} - Power: {card.power}")
