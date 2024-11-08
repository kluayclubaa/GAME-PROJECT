class Deck:
    def __init__(self, collection):
        self.collection = collection
        self.deck_cards = {}

    def load_deck(self, file_path="D:/Workspace/GAME-PROJECT/pygame-cardtest/deck.txt"):
        """Load deck from a file"""
        try:
            with open(file_path, "r") as file:
                for line in file:
                    word = line.strip()
                    if word in self.deck_cards:
                        self.deck_cards[word] += 1
                    else:
                        self.deck_cards[word] = 1
        except FileNotFoundError:
            print(f"Deck file not found at {file_path}")